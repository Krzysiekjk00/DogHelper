from django.urls import path

from doghelp.views import LoginView, TestView, LogoutView, NewUserView, VideosView

app_name = 'doghelp'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('new_user/', NewUserView.as_view(), name='new_user'),
    path('test/', TestView.as_view(), name='test'),
    path('<int:user_id>/videos/', VideosView.as_view(), name='videos')
    # path('<int:user_id>/new_case/', NewCaseView.as_view(), name='new_case')
]
