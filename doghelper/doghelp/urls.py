from django.urls import path

from doghelp.views import LoginView, test

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('test', test, name='test')
]
