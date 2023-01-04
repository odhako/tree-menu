from django import template
from django.utils.html import mark_safe
from tree_menu.models import Menu, Node


register = template.Library()


@register.simple_tag
def draw_menu(name):
    menu = Menu.objects.get(name=name)
    output = [f'<h2>{menu.display_name}</h2><ul>']

    for child in menu.children.all():
        output.append(f'<li><a href={child.url}>{child.name}</a></li>')
        if child.children.all():
            output.append('<ul>')
            for _ in child.children.all():
                output.append(f'<li><a href={_.url}>{_.name}</a></li>')
            output.append('</ul>')
        output.append('</li>')

    output.append('</ul>')
    output = "".join(output)
    return mark_safe(output)
