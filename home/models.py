from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                        PageChooserPanel, StreamFieldPanel,
                                        InlinePanel,
                                        ObjectList, TabbedInterface,)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField, RichTextField

from wagtail.contrib.routable_page.models import route, RoutablePageMixin
from streams import blocks


class HomeCarouselPage(Orderable):

    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        'wagtailimages.Image', blank=False, null=True,
        on_delete=models.SET_NULL,related_name="+")

    panels = [
        ImageChooserPanel("carousel_image"),
    ]

class HomePage(RoutablePageMixin, Page):

    subpage_types = ["blog.BlogListingPage", 'contact.ContactPage',
    'flex.FlexPage']

    parent_page_types = [
        'wagtailcore.Page',
    ]
    #max_count = 1



    banner_title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.TextField(blank=True,null=True)
    profile_image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True,
        on_delete=models.SET_NULL,related_name="+")

    banner_cta = models.ForeignKey(
        "wagtailcore.Page", blank=True,null=True,on_delete=models.SET_NULL,
        related_name="+")

    content = StreamField(
        [
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel("carousel_images", max_num=5, min_num=1, label="Image"),
        ], heading="Carousel images"),
        StreamFieldPanel("content"),
    ]


    template = "home/home_page.html"


    banner_panels = [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("subtitle"),
            PageChooserPanel("banner_cta"),
            ImageChooserPanel("profile_image"),
        ],heading="Profile content"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(banner_panels, heading="Banner Settings"),
            ObjectList(Page.promote_panels, heading="Promotional"),
            ObjectList(Page.settings_panels, heading="Settings Center"),
        ]
    )

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"


    @route(r'^subscribe/$')
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        return render(request, "home/subscribe.html", context)
