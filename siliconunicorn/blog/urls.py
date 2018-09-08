from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('', views.MostRecentEntriesList.as_view(), name='home'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('new/', views.NewPost.as_view(), name='new_post'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('blog/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('ajax/comment/add', views.ajax_comment_add, name="add_comment"),
    path('ajax/comment/delete', views.ajax_comment_delete, name="delete_comment"),
    path('ajax/comment/edit', views.ajax_comment_edit, name="edit_comment"),
    path('ajax/post/heart', views.ajax_post_heart, name="heart_post"),
]
