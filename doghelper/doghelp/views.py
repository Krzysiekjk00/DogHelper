from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse

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
            else:
                return HttpResponseRedirect(request, 'doghelp/login.html', login_ctx)


def test(request):
    return HttpResponse('It works!')
