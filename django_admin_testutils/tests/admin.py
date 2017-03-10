# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db import models
from django import forms

from .models import Author, Book, Publisher


class BookInline(admin.TabularInline):
    model = Book
    formfield_overrides = {
        models.PositiveIntegerField: {"widget": forms.HiddenInput},
    }
    sortable_field_name = "position"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]


admin.site.register(Publisher, admin.ModelAdmin)
