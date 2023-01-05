from django import template
from django.urls import reverse
from django.utils.html import mark_safe
from tree_menu.models import Menu, Node


register = template.Library()


def make_item_html(child, current_path):
    if child.url:
        url = child.url
    else:
        url = reverse(child.named_url)

    if url == current_path:
        output = f'<li><a href={url}><b>{child.name}</b></a></li>'
    else:
        output = f'<li><a href={url}>{child.name}</a></li>'

    return output


@register.simple_tag(takes_context=True)
def draw_menu(context, name):
    menu = Menu.objects.get(name=name)
    output = [f'<h2>{menu.display_name}</h2><ul>']

    for child in menu.children.all():
        output.append(make_item_html(child, context.request.path))
        if child.children.all():
            output.append('<ul>')
            for _ in child.children.all():
                output.append(make_item_html(_, context.request.path))
            output.append('</ul>')
        output.append('</li>')

    output.append('</ul>')
    output = "".join(output)
    return mark_safe(output)
