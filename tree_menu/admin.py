from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe

from .models import Menu, Node


class EditLinkToInlineObject:
    def edit_link(self, object):
        url = reverse(
            f'admin:{object._meta.app_label}_{object._meta.model_name}_change',
            args=[object.pk]
        )
        if object.pk:
            return mark_safe(f'<a href="{url}">Edit sub-items</a>')
        else:
            return ''


class ChildrenInline(EditLinkToInlineObject, admin.StackedInline):
    model = Node
    readonly_fields = ('edit_link',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ChildrenInline]


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'parent_node', 'parent_menu']
    inlines = [ChildrenInline]
