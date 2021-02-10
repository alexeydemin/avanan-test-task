from django.db import models


class Pattern(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Entry(models.Model):
    pattern_title = models.CharField(max_length=255, null=True, blank=True)
    pattern_content = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)
