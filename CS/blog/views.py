from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from .forms import PostForm, CommentForm
from .models import Post
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignupForm
from .models import Post, Comment


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Use the `related_name` we defined

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Associate comment with the post
            comment.author = request.user  # Set author to logged-in user
            comment.save()
            return redirect('post_detail', post_id=post.id)  # Reload page

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save yet
            post.author = request.user  # Assign the logged-in user as the author
            post.save()  # Now save it
            return redirect("home")  # Redirect after successful post creation
    else:
        form = PostForm()

    return render(request, "blog/create_post.html", {"form": form})



def frontpage(request):
    posts = Post.objects.all()  # Fetch all posts

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            # Create an instance but don't save to the database yet
            post = form.save(commit=False)

            # Generate a slug from the title
            post.slug = slugify(post.title)

            # Ensure the slug is unique by checking if it already exists in the database
            original_slug = post.slug
            counter = 1
            while Post.objects.filter(slug=post.slug).exists():
                post.slug = f"{original_slug}-{counter}"
                counter += 1

            # Save the post to the database
            post.save()

            # Redirect to the frontpage view
            return redirect("frontpage")

    else:
        form = PostForm()

    return render(request, "blog/frontpage.html", {"posts": posts, "form": form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm


def is_admin(user):
    return user.is_superuser  # Only allow admins

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to home page
        else:
            return render(request, "blog/login.html", {"error": "Invalid username or password."})

    return render(request, "blog/login.html")


@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')



def home(request):
    # Fetch latest 6 posts
    top_posts = Post.objects.order_by('-created_at')[:6]
    
    # Fetch the rest of the posts (excluding top 6)
    other_posts = Post.objects.order_by('-created_at')[6:]

    # Debugging: Print the posts to the terminal
    print("Top Posts:", top_posts)
    print("Other Posts:", other_posts)

    return render(request, 'blog/home.html', {
        'top_posts': top_posts,
        'other_posts': other_posts
    })

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            return redirect("home")  # Redirect to the home page or any other page
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! 🎉")
            return redirect('home')
        else:
            messages.error(request, "Error creating account. Please check the form.")
    else:
        form = SignupForm()

    return render(request, 'blog/signup.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        body = request.POST.get("body")
        if body:
            Comment.objects.create(post=post, author=request.user, body=body)
    return redirect("post_detail", post_id=post.id)

def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/all_posts.html', {'posts': posts})