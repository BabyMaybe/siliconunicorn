from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns =  [
    path('', views.MostRecentEntriesList.as_view() , name='home'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('new/', views.NewPost.as_view(), name='new_post'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('blog/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
