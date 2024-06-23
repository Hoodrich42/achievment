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
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            subscription = Profile(user=new_user, slug=new_user.username)
            subscription.save()
            login(self.request, new_user)
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

    def post(self, request, *args, **kwargs):
        which_form_is_submiting = request.POST['which_form_is_it']
        if which_form_is_submiting == 'profile_photo':
            form = ProfilePhoto(request.POST)
        else:
            form = SubscribeForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        which_form_is_submiting = self.request.POST["which_form_is_it"]
        profile = Profile.objects.get(user_id=self.request.user.id)
        print(which_form_is_submiting, '!!!!!!!!!!!!!!!!!!!!')
        if which_form_is_submiting == 'profile_photo':
            if profile.profile_image:
                file_path = str(BASE_DIR) + profile.profile_image.url
                print(file_path, 'file_pathfile_pathfile_pathfile_pathfile_path')
                os.remove(file_path)
            profile.profile_image = self.request.FILES['profile_image']
            profile.save()
            return redirect('profile', username_slug=profile.slug)

        if which_form_is_submiting == 'subscribe':
            user_profile = Profile.objects.get(slug=self.kwargs['username_slug'])
            profile.subscribe_to_user.add(user_profile.user.id)
            user_profile.subscribe_from_user.add(profile.user.id)
            return redirect('profile', username_slug=user_profile.slug)

        if which_form_is_submiting == 'unsubscribe':
            user_profile = Profile.objects.get(slug=self.kwargs['username_slug'])
            profile.subscribe_to_user.remove(user_profile.user.id)
            user_profile.subscribe_from_user.remove(profile.user.id)
            return redirect('profile', username_slug=user_profile.slug)


    def get_queryset(self):
        return Profile.objects.filter(slug=self.kwargs['username_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        context['profile'] = Profile.objects.get(user_id=self.request.user.id)
        context['user_profile'] = Profile.objects.get(slug=self.kwargs['username_slug'])
        context['sub_form'] = SubscribeForm()
        context['unsub_form'] = SubscribeForm()
        context['file'] = self.request.FILES
        context['sub_or_not'] = context['profile'].sub_or_not(context['user_profile'].user.id)
        return context

def logout_user(request):
    logout(request)
    return redirect('login')

