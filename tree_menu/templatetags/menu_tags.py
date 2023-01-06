from django import template
from django.urls import reverse
from django.utils.html import mark_safe

from tree_menu.models import Menu


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
    html += draw_node_children(node, current_url)
    return f'<li>{html}</li>'


def draw_node_children(node, current_url):
    children = node.children.all()
    if not children:
        return ''
    html = '<ul>'
    for child in children:
        html += make_node(child, current_url)
    html += '</ul>'
    return html


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    menu = Menu.objects.get(name=menu_name)
    root_nodes = menu.nodes.filter(parent=None)
    current_url = context.request.path

    html = '<ul>'
    for root_node in root_nodes:
        html += make_node(root_node, current_url)
    html += '</ul>'
    return mark_safe(html)
