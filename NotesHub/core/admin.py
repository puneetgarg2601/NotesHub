from django.contrib import admin
from .models import Course, Notes, Bookmark

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name')
    search_fields = ('course_code', 'course_name')
    ordering = ('course_code',)

class NotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'course', 'created_at', 'upvotes', 'downvotes')
    search_fields = ('title', 'description', 'user__username', 'course__course_name')
    list_filter = ('user', 'course', 'created_at')
    ordering = ('-created_at',)

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'notes', 'created_at')
    search_fields = ('user__username', 'notes__title')
    list_filter = ('user', 'created_at')
    ordering = ('-created_at',)

# Register models with custom admin classes
admin.site.register(Course, CourseAdmin)
admin.site.register(Notes, NotesAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
