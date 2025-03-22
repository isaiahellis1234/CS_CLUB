from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Post, Comment
admin.site.unregister(User)  # Unregister the default UserAdmin
admin.site.register(User, UserAdmin)  # Re-register with custom settings if needed
admin.site.register(Post)
admin.site.register(Comment)
