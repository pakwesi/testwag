from django.db import models
from django.shortcuts import render
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import route, RoutablePageMixin
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.snippets.edit_handlers import SnippetChooserPanel

from streams import blocks

# Create your models here.


class BlogAuthorsOrderable(Orderable):

    page = ParentalKey("blog.BlogDetailPage", related_name='blog_authors')
    author = models.ForeignKey(
        "blog.BlogActhor", on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]


class BlogActhor(models.Model):

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
    'wagtailimages.Image', blank=True, null=True,on_delete=models.SET_NULL,
    related_name='+')

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image"),
            ], heading="Name and Image"
        ),
        MultiFieldPanel([
            FieldPanel("website"),
        ], heading="Links")
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Acthor"
        verbose_name_plural = "Blog Acthors"

register_snippet(BlogActhor)

class BlogCategory(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(verbose_name="slug", allow_unicode=True,
                    max_length=255, help_text="A slug to identify posts by this category")


    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]


    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

register_snippet(BlogCategory)



class BlogListingPage(RoutablePageMixin, Page):

    max_count = 1

    subpage_types = [
    "blog.VideoBlogPage", 'blog.ArticleBlogPage',
    ]

    template = "blog/blog_listing_page.html"


    custom_title = models.CharField(max_length=100, blank=False,
                                    null=False, help_text="Overwrite this")

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_posts, 5)

        all_posts = BlogDetailPage.objects.live().public()

        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tag__slug__in=[tags])

        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts

        context["categories"] = BlogCategory.objects.all()
        return context

    @route(r'^latest/$', name="latest_posts")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["latest_posts"] = BlogDetailPage.objects.live()[:2]
        return render(request, "blog/latest_post.html", context)

    def get_sitemap_urls(self, request):
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_posts"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
            }
        )
        return sitemap


class BlogPageTag(TaggedItemBase):

    content_object = ParentalKey(
        'BlogDetailPage',
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogDetailPage(Page):

    subpage_types = []

    parent_page_types = [
        "blog.BlogListingPage",
    ]

    tags = ClusterTaggableManager(through=BlogPageTag,
    blank=True)

    custom_title = models.CharField(max_length=100, blank=False,
                                    null=True, help_text="Overwrite this")
    blog_image = models.ForeignKey(
    "wagtailimages.Image", blank=False, null=True, related_name='+',
    on_delete=models.SET_NULL,)

    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("cards", blocks.CardBlock( )),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("tags"),
        ImageChooserPanel("blog_image"),
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author", min_num=1, max_num=4),
        ], heading="Authors"),
        StreamFieldPanel("content"),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        ], heading="Categories")
    ]


class ArticleBlogPage(BlogDetailPage):

    template = "blog/article_blog_page.html"

    subtitle = models.CharField(max_length=100,blank=True, null=True)
    intro_image = models.ForeignKey(
        "wagtailimages.Image", blank=True, null=True,on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("subtitle"),
        FieldPanel("tags"),
        ImageChooserPanel("intro_image"),
        ImageChooserPanel("blog_image"),
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author", min_num=1, max_num=4),
        ], heading="Authors"),
        StreamFieldPanel("content"),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        ], heading="Categories")
    ]


class VideoBlogPage(BlogDetailPage):

    template = "blog/video_blog_page.html"
    youtube_video_id = models.CharField(max_length=50)


    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("blog_image"),
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author", min_num=1, max_num=4),
        ], heading="Authors"),
        StreamFieldPanel("content"),
        FieldPanel("youtube_video_id"),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        ], heading="Categories")
    ]
