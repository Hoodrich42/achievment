from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import *
from .models import *


class Main(TemplateView):
    template_name = 'purpose/base.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'purpose/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        print(context)
        return context

    def form_valid(self, form):
        user = form.save()
        subscription = Subscription(from_user=user)
        subscription.save()
        login(self.request, user)
        return redirect('main')
