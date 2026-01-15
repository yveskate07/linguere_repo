from .models import Fab_User


def get_user_id(request):
    
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = 'anonymous_id'
    
    return dict(
        user_id=user_id
    )
