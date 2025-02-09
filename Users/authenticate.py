from django.contrib.auth.backends import BaseBackend
from .models import Users
from django.contrib.auth.hashers import check_password


class TokenBackend(BaseBackend):
    def authenticate(self, request, username = None, password = None):
        try:
            user = Users.objects.get(username = username)
            if check_password(password, user.password):
                return user
        except Users.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try: 
            return Users.objects.get(pk = user_id)
        except Users.DoesNotExist:
            return None
        