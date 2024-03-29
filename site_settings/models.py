from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

# Create your models here.

@register_setting
class SocialMediaSettings(BaseSetting):

    facebook = models.URLField(blank=True, null=True, help_text="facebook Url")
    twitter = models.URLField(blank=True, null=True, help_text="twitter Url")
    youtube = models.URLField(blank=True, null=True, help_text="youtube Url")

    panels = [
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("youtube"),
        ], heading="Social media Settings")
    ]
