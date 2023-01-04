from django.contrib import admin
from .models import Menu, Node


class ChildrenInline(admin.StackedInline):
    model = Node


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ChildrenInline]


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'parent_node', 'parent_menu']
    inlines = [ChildrenInline]
