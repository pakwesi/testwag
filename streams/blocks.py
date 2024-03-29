from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):

    blocktitle = blocks.CharBlock(required=True, help_text="Add title")
    text = blocks.TextBlock(required=True, help_text="add text")

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"

class RichtextBlock(blocks.RichTextBlock):


    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Full RichText"


class CardBlock(blocks.StructBlock):
    cardtitle = blocks.CharBlock(required=True, help_text="Add title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Staff Cards"

class CTABlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True,max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default="Learn more", max_length=40)

    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"


class LinkStructValue(blocks.StructValue):

    def url(self):
        button_page = self.get("button_page")
        button_url = self.get("button_url")

        if button_page:
            return button_page
        elif button_url:
            return button_url
        return None

class ButtonBlock(blocks.StructBlock):

    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)


    class Meta:
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue
