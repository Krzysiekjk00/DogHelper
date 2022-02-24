from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from doghelp.forms import LoginForm, NewUserForm, VideosForm
from doghelp.models import Video

# Create your views here.


class LoginView(View):

    def get(self, request):
        login_ctx = {
            'form': LoginForm()
        }
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
                form.add_error(field=None, error='Wrong Username or Password. Try again.')
        login_ctx = {
            'form': form
        }
        return render(request, 'doghelp/login.html', login_ctx)


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('doghelp:login'))


class NewUserView(View):

    def get(self, request):
        ctx = {
            'form': NewUserForm()
        }
        return render(request, 'doghelp/new_user.html', ctx)

    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            is_specialist = form.cleaned_data['is_specialist']
            del form.cleaned_data['is_specialist']
            del form.cleaned_data['repassword']
            user = User.objects.create_user(**form.cleaned_data)
            if is_specialist:
                group = Group.objects.get(name='Specialist')
            else:
                group = Group.objects.get(name='Common')
            group.user_set.add(user)
            return HttpResponseRedirect(reverse('doghelp:login'))
        ctx = {
            'form': form
        }
        return render(request, 'doghelp/new_user.html', ctx)


class TestView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'doghelp/test.html')

    def post(self, request):
        return HttpResponseRedirect(reverse('doghelp:logout'))


class VideosView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        ctx = {
            'form': VideosForm(),
            'user': User.objects.get(id=user_id)
        }
        return render(request, 'doghelp/videos.html', ctx)

    def post(self, request, user_id):
        form = VideosForm(request.POST, request.FILES)
        # raise Exception(form, form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('doghelp:test'))
        return render(request, 'doghelp/test.html')



# class NewCaseView(LoginRequiredMixin, View):
#
#     def get(self, request, user_id):
#         return render(request, 'doghelp/new_case.html')
#
#     def post(self, request, user_id):
