from django.contrib.auth.models import User as UserModel


class EmailBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
            return None

        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        
        except UserModel.DoesNotExist:
            return None
