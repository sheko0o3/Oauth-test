from django.contrib import admin

from .models import Book



admin.autodiscover()
admin.site.register(Book)