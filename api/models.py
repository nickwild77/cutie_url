from django.db import models


class URL(models.Model):
    long_url = models.URLField(max_length=200)
    short_url = models.URLField(max_length=8, unique=True)
    click_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.click_count += 1
        self.save()

    def __str__(self):
        return f"{self.long_url} -> {self.short_url}"
