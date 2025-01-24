from . import views
from django.urls import path
from .views import PostCreateView

urlpatterns = [
    path("subscribe/", views.subscribe, name="subscribe"),
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
    path('<slug:slug>/edit_comment/<int:comment_id>',
         views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>',
         views.comment_delete, name='comment_delete'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/Edit', views.post_edit, name='post_edit'),
    path('<slug:slug>/Delete', views.post_delete, name='post_delete'),
]