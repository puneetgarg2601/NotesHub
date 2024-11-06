from django.db import models
from django.contrib.auth.models import User  # Assuming you're using the default User model

class Course(models.Model):
    course_code = models.CharField(
        max_length=10,
        primary_key=True,
        unique=True,
        blank=False,
        verbose_name="Course Code"
    )
    course_name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name="Course Name"
    )
    short_name = models.CharField(
        max_length=16,
        blank=False,
        verbose_name="Short Name"
    )

    description = models.CharField(
        max_length=256,
        blank=False,
        verbose_name="Course Description"
    )

    def save(self, *args, **kwargs):
        self.course_code = self.course_code.upper()
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_code}: {self.course_name}"

class Notes(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    download_url = models.URLField(max_length=500)
    preview_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500)
    view_count = models.IntegerField(default=0)
    total_time_spent = models.IntegerField(default=0)
    downloaded_times = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Define a unique constraint that combines user and notes
        unique_together = ('user', 'notes')
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"

    def __str__(self):
        return f"{self.user.username}_{self.notes.id}"