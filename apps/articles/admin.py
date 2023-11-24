from django.contrib import admin
from apps.articles.models import Article, Category, Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
