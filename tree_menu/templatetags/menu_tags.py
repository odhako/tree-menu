from django import template
from django.utils.html import mark_safe
from tree_menu.models import Menu, Node


register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, name):
    menu = Menu.objects.get(name=name)
    output = [f'<h2>{menu.display_name}</h2><ul>']
    print('Path: ', context.request.path)

    for child in menu.children.all():
        if child.url == context.request.path:
            output.append(f'<li><a href={child.url}><b>{child.name}</b></a></li>')
        else:
            output.append(f'<li><a href={child.url}>{child.name}</a></li>')
        if child.children.all():
            output.append('<ul>')
            for _ in child.children.all():
                if _.url == context.request.path:
                    output.append(f'<li><a href={_.url}><b>{_.name}</b></a></li>')
                else:
                    output.append(f'<li><a href={_.url}>{_.name}</a></li>')
            output.append('</ul>')
        output.append('</li>')

    output.append('</ul>')
    output = "".join(output)
    return mark_safe(output)
