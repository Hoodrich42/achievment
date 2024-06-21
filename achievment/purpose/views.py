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

def get_user_id(request):
    return request.user.id


class Main(TemplateView):
    template_name = 'purpose/base.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
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
        subscription = Profile(user=user)
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


class UserProfile(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'purpose/profile.html'

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        context['profile'] = Profile.objects.get(user_id=self.request.user.id)
        return context

def logout_user(request):
    logout(request)
    return redirect('login')

