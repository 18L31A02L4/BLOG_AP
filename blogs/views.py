from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_list_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from blogs.models import Post, Comment
from blogs.forms import PostForm, CommentForm
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView) 
from django.urls import reverse_lazy , reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
# Create your views here.

class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'

    def get_queryset(self) ->QuerySet[Any] :
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
    


class PostDetailView(DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    template_name = 'blog/post_form.html'
    form_class = PostForm
    model = Post  
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    template_name = 'blog/post_form.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    success_url = 'blog/post_draft_list.html'

    model = Post

    def get_queryset(self) -> QuerySet[Any]:
        return Post.objects.filter(published_date__isnull = True).order_by('created_date')
    


@login_required
def Post_publish(request,pk):
    post = get_list_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_Comment_to_Post(request,pk):
    post = get_list_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post
            comment.save()

            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return redirect(request,'blog/comment_form.html',{'form': form})

@login_required
def Comment_approve(request,pk):
    comment = get_list_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def Comment_remove(request,pk):
    comment = get_list_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()

    return redirect('post_detail', pk=post_pk)




