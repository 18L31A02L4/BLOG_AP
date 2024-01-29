"""
URL configuration for Blog_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blogs.views import *
from django.contrib.auth import views

urlpatterns = [
    path('',PostListView.as_view(),name='post_list'),
    path('about/',AboutView.as_view(),name='about'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('drafts/', DraftListView.as_view(), name='post_draft_list'),
    path('post/<int:pk>/remove/', PostDeleteView.as_view(), name='post_remove'),
    path('post/<int:pk>/Publish',Post_publish,name='Post_publish'),
    path('post/<int:pk>/comment', add_Comment_to_Post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve', Comment_approve, name='Comment_approve'),
    path('comment/<int:pk>/remove',Comment_remove,name='Comment_remove'),
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/',views.LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),
   
]
