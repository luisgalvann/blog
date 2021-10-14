from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from .models import Post
import re


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'  # nombre de la variable de la template
    ordering = ['-date']  # orden inverso
    paginate_by = 5  # sólo muestra 5 (el resto están ocultos)


class PostDetailView(DetailView):
    model = Post


# 'LoginRequiredMixin' (equivale al decorador 'login_required')
# impide acceder a la view si no se está autenticado
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):  # sobrescribimos el método 'form_valid'
        form.instance.author = self.request.user  # el autor será el user loggeado
        return super().form_valid(form)


# 'UserPassesTestMixin' impide que un usuario modifique posts de otro usuario
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):  # 'user' igual a 'user actual'
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')


class SearchPostListView(ListView):
    model = Post
    template_name = 'blog/post_search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        text = self.request.GET.get('search-text', False)
        return Post.objects.filter(content__icontains=text).order_by('-date')

    def get_context_data(self):
        context = super().get_context_data()
        path = self.request.get_full_path()
        path = re.sub('&page=.*', '', path) #recortamos los parámetros de 'pages'
        context['path'] = path # pasamos a la view el path con el parámetro de 'search' (para la paginación)
        return context
