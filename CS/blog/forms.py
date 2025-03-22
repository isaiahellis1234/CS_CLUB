from django import forms

from .models import Comment, Post
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']  # Add 'image' field

    image = forms.ImageField(required=False)  # Optional image upload



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        
        
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']