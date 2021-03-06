from django.urls import path

from doghelp.views import LoginView, LogoutView, NewUserView, AddVideosView, ChangePasswordView, MainPageView, VideoDetailsView, DeleteVideoView,\
    VideoNameUpdateView, AddCaseView, CaseDetailsView, DeleteCaseView, UpdateCaseView

app_name = 'doghelp'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('new_user/', NewUserView.as_view(), name='new_user'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('main/', MainPageView.as_view(), name='main'),
    path('add_video/', AddVideosView.as_view(), name='add_video'),
    path('videos/<int:pk>/', VideoDetailsView.as_view(), name='video_details'),
    path('videos/<int:pk>/delete/', DeleteVideoView.as_view(), name='delete_video'),
    path('videos/<int:pk>/update', VideoNameUpdateView.as_view(), name='update_video_name'),
    path('add_case/', AddCaseView.as_view(), name='add_case'),
    path('cases/<int:pk>', CaseDetailsView.as_view(), name='case_details'),
    path('cases/<int:pk>/delete/', DeleteCaseView.as_view(), name='delete_case'),
    path('cases/<int:pk>/update', UpdateCaseView.as_view(), name='update_case')
]
