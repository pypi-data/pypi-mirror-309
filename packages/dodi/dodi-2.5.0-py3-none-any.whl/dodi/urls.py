from django.urls import re_path

from ._views import image_view

urlpatterns = [re_path(r"^(?P<transform>.*)$", image_view, name="dodi_image")]
