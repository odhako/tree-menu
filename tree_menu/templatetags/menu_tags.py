from django import template
from django.utils.html import mark_safe

from tree_menu.models import Menu


register = template.Library()


def draw_node_children(node):
    children = node.children.all()
    if not children:
        return ''
    html = '<ul>'
    for child in children:
        html += '<li>'
        html += f'<a href="{child.url}">{child.name}</a>'

        # Recursive walk
        html += draw_node_children(child)
        html += '</li>'
    html += '</ul>'
    return html


@register.simple_tag
def draw_menu(menu_name):

    menu = Menu.objects.get(name=menu_name)
    root_nodes = menu.nodes.filter(parent=None)

    html = '<ul>'

    for root_node in root_nodes:
        html += '<li>'
        html += f'<a href="{root_node.url}">{root_node.name}</a>'

        # Recursive walk
        html += draw_node_children(root_node)

        html += '</li>'

    html += '</ul>'
    return mark_safe(html)
