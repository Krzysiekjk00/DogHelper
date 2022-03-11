from django.contrib.auth.mixins import UserPassesTestMixin
from doghelp.models import Case


class UserVideoPermTestMixin(UserPassesTestMixin):  # TO DO: The mixin seems to look pretty the same - maybe it is possible to do one.

    def test_func(self):
        video_id = self.kwargs.get('pk')
        user_video_ids = [video.id for video in self.request.user.videos.all()]
        return video_id in user_video_ids


class UserCaseFullPermTestMixin(UserPassesTestMixin):

    def test_func(self):
        case_id = self.kwargs.get('pk')
        user_cases_ids = [case.id for case in self.request.user.cases.all()]
        return case_id in user_cases_ids


class UserCaseViewPermTestMixin(UserPassesTestMixin):

    def test_func(self):
        case_id = self.kwargs.get('pk')
        case = Case.objects.get(pk=case_id)
        user_cases_ids = [case.id for case in self.request.user.cases.all()]
        if case.is_public or case_id in user_cases_ids:
            return True
        else:
            return False
