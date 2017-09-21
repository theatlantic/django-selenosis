# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
try:
    # Django 1.10
    from django.urls import reverse
except ImportError:
    # Django <= 1.9
    from django.core.urlresolvers import reverse


@python_2_unicode_compatible
class Publisher(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=50)

    @classmethod
    def get_admin_changelist_url(cls):
        info = (cls._meta.app_label, cls._meta.model_name)
        return reverse("admin:%s_%s_changelist" % info)

    @classmethod
    def get_admin_add_url(cls):
        info = (cls._meta.app_label, cls._meta.model_name)
        return reverse("admin:%s_%s_add" % info)

    def get_admin_change_url(self):
        info = (type(self)._meta.app_label, type(self)._meta.model_name)
        return reverse("admin:%s_%s_change" % info, args=[self.pk])

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Book(models.Model):
    name = models.CharField(max_length=50)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name
