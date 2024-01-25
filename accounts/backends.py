from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, user_type = None, uni_id = None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username, user_type=user_type, uni_id = uni_id)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None