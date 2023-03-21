from rest_framework_simplejwt.tokens import RefreshToken


def create_jwt_pair(user):
    refresh = RefreshToken.for_user(user)

    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }

    return tokens
