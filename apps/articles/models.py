from autoslug import AutoSlugField
from django.db import models
from tinymce.models import HTMLField
from apps.accounts.models import User
from apps.common.models import TimeStampedUUIDModel


def upload_dir(instance, filename):
    return f"article_photos/{instance.user.username}/{filename}"


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Article(TimeStampedUUIDModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='id', unique_with='title', unique=True, always_update=True)
    description = models.TextField()
    content = HTMLField()
    image = models.ImageField(upload_to=upload_dir, blank=True, null=True)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    created = models.DateField(auto_created=True)
    view_count = models.PositiveIntegerField(default=0)  # Add this field

    def __str__(self):
        return self.title

    def increment_view_count(self):
        self.view_count += 1
        self.save()

    def image_url(self):
        if self.image:
            return self.image.url
        return 'https://res.cloudinary.com/geetechlab-com/image/upload/v1669891586/propertyDealzin9ja/real-estate-gc753deb4c_1280_mqjpk8.jpg'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comments')
    author = models.ForeignKey(User, related_name='article_comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"
