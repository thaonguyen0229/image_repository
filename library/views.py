from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView
    )
from .models import Post

def public_library(request):
    posts = Post.objects.filter(public=True)
    context = {
        'title': 'Public Library',
        'posts': posts,
        }
    return render(request, 'library/publiclibrary.html', context)


class PostDetailView(DetailView):
    model = Post


class PostCreatelView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','public','image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class PostUpdatelView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','public','image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.owner

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.owner