from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.views import generic

from .forms import BlogCommentForm
from .models import Blog, BlogComment


class PostListView(generic.ListView):
    template_name = 'blogs/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 3

    def get_queryset(self):
        return Blog.objects.filter(status=Blog.BLOG_STATUS_PUBLISHED).select_related('author__user')


class PostDetailView(generic.DetailView):
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = BlogCommentForm()
        recent_posts = Blog.objects.filter(status=Blog.BLOG_STATUS_PUBLISHED).values('img', 'title', 'date_created',)[:2]
        context['recent_posts'] = recent_posts
        return context

    def post(self, request, *args, **kwargs):
        coment_form = BlogCommentForm(request.POST)
        if coment_form.is_valid():
            parent_id = request.POST.get('parent_id')
            new_comment = coment_form.save(commit=False)
            new_comment.author = self.request.user
            new_comment.blog = self.get_object()
            new_comment.parent_id = parent_id
            new_comment.save()
            return redirect(self.get_object().get_absolute_url())

    def get_queryset(self):
        blog_queryset = Blog.objects.filter(pk=self.kwargs['pk'], slug=self.kwargs['slug'],
                                            status=Blog.BLOG_STATUS_PUBLISHED).select_related(
            'author'
        ). \
            prefetch_related(Prefetch('comments',
                                      queryset=BlogComment
                                      .objects
                                      .filter(status=True)
                                      .select_related(
                                          'author', 'parent')
                                      .prefetch_related(
                                          'replies__author'
                                      )
                                      )
                             )

        return blog_queryset
