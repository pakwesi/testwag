from django.db import models

# Create your models here.
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from streams import blocks

class FlexPage(Page):

    parent_page_types = [
    'flex.FlexPage', 'home.HomePage',
    ]

    subpage_types = ['flex.FlexPage', 'contact.ContactPage']

    template = "flex/flex_page.html"

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("cards", blocks.CardBlock( )),
            ("cta", blocks.CTABlock()),
            ("button", blocks.ButtonBlock()),
        ],
        null=True,
        blank=True)

    newsubtitle = models.CharField(max_length=100, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("newsubtitle"),
        StreamFieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
