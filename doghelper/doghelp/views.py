from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from doghelp.forms import LoginForm
from doghelp.contexts.doghelp.context import login_ctx

# Create your views here.


class LoginView(View):

    def get(self, request):
        return render(request, 'doghelp/login.html', login_ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                url = request.GET.get('next')
                if url:
                    return redirect(url)
                return HttpResponseRedirect(reverse('doghelp:test'))
            else:
                return HttpResponseRedirect(request, 'doghelp/login.html', login_ctx)


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('doghelp:login'))


class TestView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'doghelp/test.html')

    def post(self, request):
        return HttpResponseRedirect(reverse('doghelp:logout'))
