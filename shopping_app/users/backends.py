from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None

        if not user.is_active:
            raise ValidationError(
                "اکانت شما فعال نمی باشد. لطفا برای وارد شدن به ورود به سایت اکانت خود را فعال نمایید.")

        if user.check_password(password):
            return user
        return None
