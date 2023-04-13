from django.contrib.auth.hashers import check_password, make_password
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


class NewsArticle(models.Model):
    news_article_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length = 255,blank=True, null=True)
    image_path = models.CharField(max_length = 1000,blank=True, null=True)
    source = models.CharField(max_length = 255,blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'News_article'