from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class SignUp(SuccessMessageMixin, CreateView):
    form_class = BaseUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/registration.html"
    extra_context = {'title': 'Create user'}
    success_message = "Вы успешно зарегестрировались! Войдите в свой аккаунт."
