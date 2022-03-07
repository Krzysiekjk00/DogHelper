from django.contrib.auth.models import User


def user(request):
    if request.user.is_authenticated:
        ctx = {
            'user': User.objects.get(pk=request.user.id)
        }
        return ctx
    else:
        return {}
