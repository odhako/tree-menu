from django import template
from django.urls import reverse
from django.utils.html import mark_safe

from tree_menu.models import Menu, Node


register = template.Library()


def get_url(node):
    if node.named_url:
        url = reverse(node.named_url)
    else:
        url = node.url
    return url


def make_node(node, current_url):
    name = node.name
    url = get_url(node)

    # Make active link bold
    if url == current_url:
        name = f'<b>{node.name}</b>'

    html = f'<a href="{url}">{name}</a>'

    # Draw children
    children = node.children.all()
    if children:
        html += '<ul>'
        for child in children:
            html += make_node(child, current_url)
        html += '</ul>'

    return f'<li>{html}</li>'


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    root_node = Menu.objects.get(name=menu_name).root_node
    current_url = context.request.path

    html = '<ul>'
    html += make_node(root_node, current_url)
    html += '</ul>'
    return mark_safe(html)
