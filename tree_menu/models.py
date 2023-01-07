from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.


class Menu(models.Model):
    name = models.CharField(
        verbose_name='Menu name',
        max_length=40,
        null=False,
        unique=True,
    )

    display_name = models.CharField(
        verbose_name='Display name',
        max_length=40,
        null=False,
        unique=False,
    )

    root_node = models.ForeignKey(
        'Node',
        on_delete=models.CASCADE,
        related_name='is_root_node',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def save(self, force_insert=False, **kwargs):
        if not self.root_node:
            root_node = Node()
            root_node.name = 'root'
            root_node.url = '/'
            if not self.pk:  # If creating new menu
                super(Menu, self).save(force_insert, **kwargs)
                force_insert = False
            root_node.menu = self
            root_node.save()  # Save, so that it gets a pk
            self.root_node = root_node
        super(Menu, self).save(force_insert, **kwargs)


class Node(models.Model):
    name = models.CharField(
        verbose_name='Node name',
        max_length=40,
        null=False,
        unique=False,
    )

    named_url = models.CharField(
        verbose_name='Named URL (used by default)',
        max_length=200,
        null=True,
        blank=True,
    )

    url = models.CharField(
        verbose_name='URL',
        max_length=200,
        null=True,
        blank=True,
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
    )

    menu = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        related_name='nodes',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def clean(self):
        if not self.url and not self.named_url:
            raise ValidationError(
                {'url': 'One of "URL" or "Named URL" should have a value.'}
            )
