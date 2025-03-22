from django.urls import path
from blog.views import signup_view, login_view, logout_view, home, frontpage, post_detail, all_posts
from django.contrib.auth.models import User
from blog.views import create_post
from .views import logout_view, post_detail, create_post

urlpatterns = [
    path('', home, name='home'),
    path("create/", create_post, name="create_post"),  # Add this URL for creating posts
    path('signup/', signup_view, name='signup'),  # Add signup route
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('frontpage/', frontpage, name='frontpage'),
    path('logout/', logout_view, name='logout'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/new/', create_post, name='post_create'),  # Add this line
    path('all-posts/', all_posts, name='all_posts'),  # Add this

]
