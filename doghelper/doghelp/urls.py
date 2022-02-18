from django.urls import path

from doghelp.views import LoginView, TestView, LogoutView

app_name = 'doghelp'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('test/', TestView.as_view(), name='test')
]
