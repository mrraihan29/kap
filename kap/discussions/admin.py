from django.contrib import admin

from .models import Comment, Discussion
# Register your models here.
admin.site.register(Comment)
admin.site.register(Discussion)