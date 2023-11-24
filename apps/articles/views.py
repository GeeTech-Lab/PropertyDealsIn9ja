from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from apps.articles.models import Article, Category, Comment
from apps.properties.models import Property


class ArticleListView(View):
    template_name = "articles/list.html"

    def get(self, request):
        articles = Article.objects.filter(published=True).order_by('-created')
        categories = Category.objects.annotate(article_count=Count('article'))
        featured_properties = Property.objects.filter(featured=True).order_by('-uploaded_at')[:3]
        print(categories)
        context = {
            "articles": articles,
            "categories": categories,
            "featured_properties": featured_properties
        }
        return render(request, self.template_name, context)


class ArticleDetailView(View):
    template_name = "articles/detail.html"

    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        featured_properties = Property.objects.filter(featured=True).order_by('-uploaded_at')[:3]
        categories = Category.objects.annotate(article_count=Count('article'))
        related_articles = Article.objects.filter(published=True, category=article.category).exclude(id=article.id).order_by('-created')[:2]
        comments = Comment.objects.filter(article=article).order_by('-created_at')
        article.increment_view_count()
        context = {
            "article": article,
            "featured_properties": featured_properties,
            "categories": categories,
            "related_articles": related_articles,
            "comments": comments
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        content = request.POST.get("content")
        print(f"comment_content: {content}")
        article = Article.objects.get(slug=slug)
        comment = Comment.objects.create(
            article=article,
            author=self.request.user,
            content=content
        )
        comment.save()
        return JsonResponse({
            "status": "success",
            "message": "Comment added successfully",
            "img": comment.author.profile.image_url,
            "author": comment.author.get_full_name,
            "created_at": comment.created_at,
            "content": comment.content
        })
