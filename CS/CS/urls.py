from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Add this
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Optional logout
    path('', include('blog.urls')),  # Make sure your app URLs are included
]


from django.conf import settings
from django.conf.urls.static import static

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)