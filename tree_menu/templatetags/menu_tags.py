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


def draw_node_children(node, current_url):
    children = node.children.all()
    if not children:
        return ''
    html = '<ul>'
    for child in children:
        name = child.name
        url = get_url(child)

        # Make active link bold
        if url == current_url:
            name = f'<b>{child.name}</b>'

        html += '<li>'
        html += f'<a href="{url}">{name}</a>'

        # Recursive walk
        html += draw_node_children(child, current_url)
        html += '</li>'
    html += '</ul>'
    return html


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):

    menu = Menu.objects.get(name=menu_name)
    root_nodes = menu.nodes.filter(parent=None)
    current_url = context.request.path

    html = '<ul>'

    for root_node in root_nodes:
        name = root_node.name
        url = get_url(root_node)

        # Make active link bold
        if url == current_url:
            name = f'<b>{root_node.name}</b>'

        html += '<li>'
        html += f'<a href="{url}">{name}</a>'

        # Recursive walk
        html += draw_node_children(root_node, current_url)

        html += '</li>'

    html += '</ul>'
    return mark_safe(html)
