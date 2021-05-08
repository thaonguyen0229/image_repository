from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from library.models import Post

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created. You are now able to log in!')
            return redirect('login')

    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})


@login_required
def my_library(request):
    posts = Post.objects.filter(owner=request.user)
    context = {
        'title': 'My Library',
        "posts": posts
        }
    return render(request, 'users/mylibrary.html', context)
