from .models import Team

def user_team(request):
    if request.user.is_authenticated:
        user_team = getattr(request.user, 'user_team', None)
        return {'user_team': user_team}
    return {}
