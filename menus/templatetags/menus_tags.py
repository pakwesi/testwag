

from ..models import Menu

from django import template

register = template.Library()

@register.simple_tag()
def get_menu(slug):
    return Menu.objects.get(slug=slug)
