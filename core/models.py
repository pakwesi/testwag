from django.db import models

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

from wagtail.core import hooks
# Create your models here.

@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():

    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/custom.css")
    )
