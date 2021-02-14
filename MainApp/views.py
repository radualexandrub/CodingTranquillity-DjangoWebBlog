from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import BlogPost, BlogComment
from .forms import NewCommentForm
from django.contrib.auth.models import User
from django.db.models import Q

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)  # class based-view

from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin)

# robots.txt
from django.views.decorators.http import require_GET

# def index(requst):
#   ''' Replaced with BlogPostListView(ListView) '''
#   context = {'posts': BlogPost.objects.order_by('-date_posted')}
#   return render(requst, "MainApp/index.html", context)

PAGINATION_COUNT = 10

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'MainApp/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'

    def get_queryset(self):
        search_input = self.request.GET.get('search')
        if search_input:
            queryset = BlogPost.objects.filter(
                Q(title__icontains=search_input) | Q(subtitle__icontains=search_input)).order_by('-date_posted')
        else:
            queryset = BlogPost.objects.order_by('-date_posted')
        return queryset

    paginate_by = PAGINATION_COUNT

class UserBlogPostListView(ListView):
    model = BlogPost
    template_name = 'MainApp/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = PAGINATION_COUNT

    def get_queryset(self):
        # if user doesn't exist return 404
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return BlogPost.objects.filter(author=user).order_by('-date_posted')

class BlogPostDetailView(DetailView):
    model = BlogPost
    # template_name = MainApp/BlogPost_detail.html
    # context_object_name = 'object'

    def get_context_data(self, **kwargs):
        ''' Manage Likes and Comments '''
        data = super().get_context_data(**kwargs)

        comments_connected = BlogComment.objects.filter(
            blogpost_connected=self.get_object()).order_by('date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)

        likes_connected = get_object_or_404(BlogPost, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data

    def post(self, request, *args, **kwargs):
        new_comment = BlogComment(content=request.POST.get('content'),
                                  author=self.request.user,
                                  blogpost_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogPost
    # template_name = 'MainApp/blogpost_form.html'
    permission_required = 'MainApp.add_blogpost'
    fields = ['title', 'subtitle', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    # template_name = 'MainApp/blogpost_form.html'
    permission_required = 'MainApp.add_blogpost'
    fields = ['title', 'subtitle', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Don't let other users with permissions update other users posts
        blogpost = self.get_object()
        if self.request.user == blogpost.author:
            return True
        return False

class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = '/'

    def test_func(self):
        # Don't let other users with permissions update other users posts
        blogpost = self.get_object()
        if self.request.user == blogpost.author:
            return True
        return False

def BlogPostLike(request, pk):
    post = get_object_or_404(BlogPost, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('blogpost-detail', args=[str(pk)]))

def about(requst):
    return render(requst, "MainApp/about.html")

def contact(requst):
    return render(requst, "MainApp/contact.html")

@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /private/",
        "Disallow: /junk/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
