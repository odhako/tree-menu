from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

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

    def __str__(self):
        return self.name


class Node(models.Model):
    name = models.CharField(
        verbose_name='Node name',
        max_length=40,
        null=False,
        unique=False,
    )

    url = models.URLField(
        verbose_name='URL',
        null=False,
        unique=False,
    )

    parent_node = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
    )

    parent_menu = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
