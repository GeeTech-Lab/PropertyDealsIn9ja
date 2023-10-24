from autoslug import AutoSlugField
from django.db import models
from apps.accounts.models import User
from apps.common.models import TimeStampedUUIDModel


def upload_dir(instance, filename):
    return f"article_photos/{instance.user.username}/{filename}"


class Article(TimeStampedUUIDModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='id', unique_with='enquiry_date', unique=True, always_update=True)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_dir, blank=True, null=True)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def image_url(self):
        if self.image:
            return self.image.url
        return 'https://res.cloudinary.com/geetechlab-com/image/upload/v1583147406/nwaben.com/user_azjdde_sd2oje.jpg'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comments')
    author = models.ForeignKey(User, related_name='article_comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"
