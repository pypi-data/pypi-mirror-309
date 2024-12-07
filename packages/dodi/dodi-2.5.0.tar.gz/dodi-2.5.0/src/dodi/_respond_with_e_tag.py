from typing import Callable

from django import http


def respond_with_e_tag(
    request: http.HttpRequest,
    etag: str,
    content_builder: Callable[[], http.HttpResponse],
    max_age: int = 31536000,  # 1 year - widely recommended maximum value
):
    """
    Return a "not-modified" response if appropriate, or delegate to content_builder.

    In either case, set appropriate caching headers on the response.
    """

    # reminder - If-None-Match header may contain multiple comma-separate e-tags.
    # Each e-tag should be quoted, so simple substring match should be sufficient
    matches = etag in request.headers.get("if-none-match", "")
    response = http.HttpResponseNotModified() if matches else content_builder()

    response["ETag"] = etag
    response["Cache-Control"] = f"public, max-age={max_age}"
    return response
