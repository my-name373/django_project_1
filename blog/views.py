from typing import Any
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'values'
    ordering = ['-date']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'values'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        new_list = Post.objects.filter(person=user)
        return new_list.order_by('-date')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['subject', 'info']

    def form_valid(self, form):
        form.instance.person = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['subject', 'info']

    def form_valid(self, form):
        form.instance.person = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.person:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.person:
            return True
        return False



def home(request):
    context = {
        'title': 'home',
        'values': Post.objects.all(),
    }
    return render(request, 'blog/index.html', context)