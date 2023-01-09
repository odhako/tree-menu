from django import template
from django.db.models import Q
from django.urls import reverse, resolve, Resolver404
from django.utils.html import mark_safe

from tree_menu.models import Menu, Node


register = template.Library()


def get_ancestors(node):  # Starts with parent node
    ancestors = []
    while node:
        ancestors.append(node)
        node = node.parent
    # ancestors = ancestors.reverse()
    return ancestors


def get_children(node):
    children = []
    for child in node.children.all():
        children.append(child)
    return children


def draw_node(node, active=False):
    if node.named_url:
        url = reverse(node.named_url)
    else:
        url = node.url
    html = '<li>'
    if active:
        html += f'<a href={url}><b>{node.name}</b></a>'
    else:
        html += f'<a href={url}>{node.name}</a>'
    html += '</li>'
    return html


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_url = context.request.path
    # print('Current path: ', current_url)

    # Get url_name
    try:
        current_url_name = resolve(current_url).url_name
    except Resolver404:
        current_url_name = None
    # print('Current named url: ', current_url_name)

    # Draw menu
    # html = '<ul>'
    html = ''

    # Get active node
    if current_url_name:
        active_node = Node.objects.filter(
            menu=Menu.objects.get(name=menu_name).id
        ).get(named_url=current_url_name)
    elif current_url:
        active_node = Node.objects.filter(
            menu=Menu.objects.get(name=menu_name).id
        ).get(url=current_url)
    # print('Active node: ', active_node)

    # Get active node parents
    i = 1  # number of </ul> in th end
    if active_node.parent:
        ancestors = get_ancestors(active_node.parent)
        # print('Ancestors: ', ancestors)

        # Draw ancestors
        i = len(ancestors) + 2
        for node in reversed(ancestors):
            html += '<ul>'
            html += draw_node(node)

    # Draw active node
    html += '<ul>'
    html += draw_node(active_node, active=True)
    html += '<ul>'

    # Get active node children
    children = get_children(active_node)
    # print('Children: ', children)

    # Draw children
    for node in children:
        html += draw_node(node)
    html += '</ul>' * i
    return mark_safe(html)
