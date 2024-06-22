import os

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, TemplateView, DetailView

from .utils import *
from .forms import *
from .models import *
from achievment.settings import BASE_DIR


class Main(TemplateView):
    template_name = 'purpose/base.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        if self.request.user.is_authenticated:
            context['profile'] = Profile.objects.get(user_id=self.request.user.id)
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'purpose/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        subscription = Profile(user=user, slug=user.username)
        subscription.save()
        login(self.request, user)
        return redirect('main')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'purpose/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context

    def get_success_url(self):
        return reverse_lazy('main')

def handle_uploaded_file(f):
    with open(f"media/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class UserProfile(DetailView, CreateView):
    model = Profile
    form_class = ProfilePhoto
    context_object_name = 'profile'
    template_name = 'purpose/profile.html'
    slug_url_kwarg = 'username_slug'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        fp = Profile.objects.get(user_id=self.request.user.id)
        if fp.profile_image:
            file_path = str(BASE_DIR) + fp.profile_image.url
            print(file_path, 'file_pathfile_pathfile_pathfile_pathfile_path')
            os.remove(file_path)
        fp.profile_image = self.request.FILES['profile_image']
        fp.save()
        return redirect('profile', username_slug=fp.slug)

    def get_queryset(self):
        return Profile.objects.filter(slug=self.kwargs['username_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        context['profile'] = Profile.objects.get(slug=self.kwargs['username_slug'])
        context['file'] = self.request.FILES
        return context

def logout_user(request):
    logout(request)
    return redirect('login')

