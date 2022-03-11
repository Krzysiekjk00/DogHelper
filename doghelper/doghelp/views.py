from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.views import View, generic
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from doghelp.forms import LoginForm, NewUserForm, AddVideosForm, NewCaseForm, UpdateCaseForm
from doghelp.models import Video, Case
from doghelp.mixins import UserVideoPermTestMixin, UserCaseFullPermTestMixin, UserCaseViewPermTestMixin

# Create your views here.

# User Views:


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
                return HttpResponseRedirect(reverse('doghelp:main'))
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
            user_data = form.cleaned_data
            user = User.objects.create_user(username=user_data['username'], email=user_data['email'], password=user_data['password1'])
            if user_data['is_specialist']:
                group = Group.objects.get(name='Specialist')
            else:
                group = Group.objects.get(name='Common')
            group.user_set.add(user)
            return HttpResponseRedirect(reverse('doghelp:login'))
        ctx = {
            'form': form
        }
        return render(request, 'doghelp/new_user.html', ctx)


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        ctx = {
            'form': PasswordChangeForm(request.user)
        }
        return render(request, 'doghelp/base.html', ctx)

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return HttpResponseRedirect(reverse('doghelp:main'))
        else:
            messages.error(request, 'Please correct the error below')  # messages are not showing up - why? TO DO
        ctx = {
            'form': form
        }
        return render(request, 'doghelp/base.html', ctx)


# Videos Views:


class MainPageView(LoginRequiredMixin, View):

    def get(self, request):
        case = Case.objects.all()
        is_specialist = 1 in [group.id for group in self.request.user.groups.all()]
        ctx = {
            'videos': Video.objects.filter(author_id=request.user).order_by('-upload_time'),
            'cases': case.filter(author_id=request.user).order_by('-last_modified'),
            'public_cases': case.filter(is_public=True).exclude(author_id=request.user),
            'unassigned_cases': case.filter(pet_specialist=None),
            'is_specialist': is_specialist
        }
        return render(request, 'doghelp/main.html', ctx)


class AddVideosView(LoginRequiredMixin, View):

    def get(self, request):
        ctx = {
            'form': AddVideosForm()
        }
        return render(request, 'doghelp/add_video.html', ctx)

    def post(self, request):
        form = AddVideosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('doghelp:main'))
        return render(request, 'doghelp/main.html')


class VideoDetailsView(LoginRequiredMixin, UserVideoPermTestMixin, generic.DetailView):
    model = Video
    template_name = 'doghelp/video_details.html'


class DeleteVideoView(LoginRequiredMixin, UserVideoPermTestMixin, generic.DeleteView):
    model = Video
    success_url = reverse_lazy('doghelp:main')


class VideoNameUpdateView(LoginRequiredMixin, UserVideoPermTestMixin, generic.UpdateView):
    model = Video
    fields = ['name']
    success_url = reverse_lazy('doghelp:main')
    template_name = 'doghelp/video_update_name.html'


#  Cases views


class AddCaseView(LoginRequiredMixin, View):

    def get(self, request):
        ctx = {
            'form': NewCaseForm(request.user)
        }
        return render(request, 'doghelp/new_case.html', ctx)

    def post(self, request):
        form = NewCaseForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('doghelp:main'))
        ctx = {
            'form': form
        }
        return render(request, 'doghelp/new_case.html', ctx)


class CaseDetailsView(LoginRequiredMixin, UserCaseViewPermTestMixin, generic.DetailView):
    model = Case
    template_name = 'doghelp/case_details.html'


class DeleteCaseView(LoginRequiredMixin, UserCaseFullPermTestMixin, generic.DeleteView):
    model = Case
    success_url = reverse_lazy('doghelp:main')


class UpdateCaseView(LoginRequiredMixin, UserCaseFullPermTestMixin, generic.UpdateView):
    model = Case
    template_name = 'doghelp/case_update.html'
    form_class = UpdateCaseForm

    def get_form_kwargs(self):
        kwargs = super(UpdateCaseView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('doghelp:case_details', kwargs={'pk': self.kwargs['pk']})
