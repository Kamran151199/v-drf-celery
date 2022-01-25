from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWT(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        if not user.is_verified:
            raise AuthenticationFailed(detail='User is not verified', code='not_verified')
        return user


def custom_user_authentication_rule(user):
    """
     JWT uses this rule to return the user object. We can modify it for our need (e.g. is_verified=True)

    :param user:
    :return:
    """
    if user:
        if not user.is_verified:
            raise AuthenticationFailed(detail='User is not verified', code='not_verified')
    return user is not None and user.is_active
