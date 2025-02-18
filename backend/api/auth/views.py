from django.contrib.auth import get_user_model
from rest_framework import permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.auth.serializers import LoginSerializer, RegisterSerializer

User = get_user_model()


class RegisterView(views.APIView):
    """Только регистрация."""
    permission_classes = [permissions.AllowAny]

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
    """Какстомная авторизация через получение токенов."""
    serializer_class = LoginSerializer


class LogoutView(views.APIView):
    """Логаут с удалением токенов."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Добавляем refresh-токен в черный список
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
