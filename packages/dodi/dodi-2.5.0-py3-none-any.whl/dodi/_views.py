from io import BytesIO
from pathlib import Path
from typing import Iterator
from urllib.parse import unquote

from django import http
from django.conf import settings
from django.contrib.staticfiles import finders
from PIL import Image, UnidentifiedImageError

from . import validator
from ._operations import transform as do_transform
from ._respond_with_e_tag import respond_with_e_tag
from .transform import Transform, TransformParseError


def iter_possible_local_file_locations(source_url: str) -> Iterator[Path]:
    source_url = unquote(source_url)

    if not source_url.startswith("/"):
        return

    static_url = getattr(settings, "STATIC_URL")
    if static_url and source_url.startswith(static_url):
        path = source_url[len(static_url) :]

        # Is it the path to a "collectstatic-ed" file? (ie. live server)
        static_root = getattr(settings, "STATIC_ROOT")
        if static_root:
            yield Path(static_root, *path.split("/"))

        # Is it an uncollected static file? (ie. dev server)
        path = finders.find(path)
        if path:
            # finders.find() returns a list if you pass all=True, otherwise a single str
            assert isinstance(path, str)

            yield Path(path)

    # Is it the path to a local media file?
    media_url = getattr(settings, "MEDIA_URL")
    media_root = getattr(settings, "MEDIA_ROOT")
    if media_url and media_root and source_url.startswith(media_url):
        path = source_url[len(media_url) :]
        yield Path(media_root, *path.split("/"))


def get_file_path(source: str) -> Path:
    for path in iter_possible_local_file_locations(source):
        if path.is_file():
            return path
    raise http.Http404()


def image_view(request: http.HttpRequest, transform: str):
    path_query = request.get_full_path().split("?", 1)
    try:
        source = path_query[1]
    except IndexError:
        source = ""

    try:
        validator.validator.validate_request(request, transform, source)
    except validator.ValidationError as e:
        return http.HttpResponseForbidden(str(e))

    # may raise 404
    source_path = get_file_path(source)

    etag = f'"{source_path.stat().st_mtime}"'

    try:
        parsed_transform = Transform.from_string(transform)
    except TransformParseError as e:
        return http.HttpResponseBadRequest(str(e))

    try:
        validator.validator.validate_parsed_transform(request, parsed_transform)
        validator.validator.validate_local_source_file(request, str(source_path))
    except validator.ValidationError as e:
        return http.HttpResponseForbidden(str(e))

    def build_response():
        try:
            image = Image.open(source_path)
        except UnidentifiedImageError:
            return http.HttpResponseBadRequest(
                b"File could not be interpereted as an image"
            )

        # Save this, because various PIL operations return a new image with no format set
        image_format = image.format

        try:
            image = do_transform(image, parsed_transform)
            content_buffer = BytesIO()
            image.save(content_buffer, image_format)
        finally:
            image.close()

        content_buffer.seek(0)

        return http.HttpResponse(
            content_buffer.read(),
            content_type=Image.MIME[image_format] if image_format else None,
        )

    return respond_with_e_tag(request, etag, build_response)
