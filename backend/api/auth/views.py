from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, views
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.auth.serializers import LoginSerializer, RegisterSerializer
from api.auth.swagger import LOGIN_SCHEMA, LOGOUT_SCHEMA, REGISTER_SCHEMA

User = get_user_model()


class RegisterView(views.APIView):
    """Только регистрация."""
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(**REGISTER_SCHEMA)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return Response(tokens, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """Авторизация пользователя."""
    serializer_class = LoginSerializer

    @swagger_auto_schema(**LOGIN_SCHEMA)
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except AuthenticationFailed as exception:
            return Response(
                {'detail': str(exception)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(views.APIView):
    """Логаут с удалением токенов."""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**LOGOUT_SCHEMA)
    def post(self, request):

        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Добавляем refresh-токен в черный список
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
