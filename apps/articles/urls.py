from django.urls import path
from . import views


urlpatterns = [
    path('<slug:slug>/', views.ArticleDetailView.as_view(), name='detail'),
    path('', views.ArticleListView.as_view(), name='list'),
]
