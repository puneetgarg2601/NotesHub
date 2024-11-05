from django.contrib import admin
from .models import Course, Notes, Bookmark

admin.site.register(Course)
admin.site.register(Notes)
admin.site.register(Bookmark)