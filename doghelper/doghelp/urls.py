from django.urls import path

from doghelp.views import LoginView, LogoutView, NewUserView, VideosView, ChangePasswordView, MainPageView, VideoDetailsView, DeleteVideoView

app_name = 'doghelp'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('new_user/', NewUserView.as_view(), name='new_user'),
    # path('test/', TestView.as_view(), name='test'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('main/', MainPageView.as_view(), name='main'),
    path('add_video/', VideosView.as_view(), name='add_video'),
    path('videos/<int:pk>/', VideoDetailsView.as_view(), name='video_details'),
    path('videos/<int:pk>/delete/', DeleteVideoView.as_view(), name='delete_video')
    # path('<int:user_id>/new_case/', NewCaseView.as_view(), name='new_case')
]
