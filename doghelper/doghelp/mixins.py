from django.contrib.auth.mixins import UserPassesTestMixin


class UserPassessPermTestMixin(UserPassesTestMixin):

    def test_func(self):
        video_id = self.kwargs.get('pk')
        user_video_ids = [video.id for video in self.request.user.videos.all()]
        return video_id in user_video_ids
