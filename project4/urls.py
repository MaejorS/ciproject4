from . import views
from django.urls import path

urlpatterns = [
    path("subscribe/", views.subscribe, name="subscribe"),
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
]