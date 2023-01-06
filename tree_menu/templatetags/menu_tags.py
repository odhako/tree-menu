from django import template
from django.utils.html import mark_safe

from tree_menu.models import Menu


register = template.Library()


def draw_node_children(node, current_url):
    children = node.children.all()
    if not children:
        return ''
    html = '<ul>'
    for child in children:
        name_with_state = child.name

        # Make active link bold
        if child.url == current_url:
            name_with_state = f'<b>{child.name}</b>'

        html += '<li>'
        html += f'<a href="{child.url}">{name_with_state}</a>'

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
        name_with_state = root_node.name

        # Make active link bold
        if root_node.url == current_url:
            name_with_state = f'<b>{root_node.name}</b>'

        html += '<li>'
        html += f'<a href="{root_node.url}">{name_with_state}</a>'

        # Recursive walk
        html += draw_node_children(root_node, current_url)

        html += '</li>'

    html += '</ul>'
    return mark_safe(html)
