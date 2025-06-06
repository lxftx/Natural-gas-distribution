from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import (RegisterUserSerializer,
                              TokenObtainPairSerializer, UserSerializer)
from user.services import CookieServices


# Create your views here.
class LoginAPIView(TokenObtainPairView):
    """
    API для аутентификации пользователей с JWT.
    Возвращает:
    - access-токен в теле ответа
    - refresh-токен в HTTP-only, Secure cookie
    """
    
    @swagger_auto_schema(
        operation_summary="Авторизация пользователя",
        operation_description="""
        Аутентификация пользователя по email и паролю.
        При успешной авторизации:
        - Возвращает access-токен в теле ответа
        - Устанавливает refresh-токен в HTTP-only cookie
        """,
        tags=["Пользователь"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Email пользователя"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Пароль пользователя"
                )
            },
            example={
                "email": "admin@gmail.com",
                "password": "admin12345"
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Успешная авторизация",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='JWT access token'
                        )
                    }
                ),
                examples={
                    "application/json": {
                        "access": "eyJhbGciOi..."
                    }
                }
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Неверные учетные данные",
                examples={
                    "application/json": {
                        "error": "Неверный email или пароль"
                    }
                }
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Внутренняя ошибка сервера",
                examples={
                    "application/json": {
                        "error": "Произошла ошибка при авторизации"
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            # Пробуем получить токены через родительский класс
            response = super().post(request, *args, **kwargs)

            custom_response = Response(
                data={"access": response.data["access"]},
                status=status.HTTP_200_OK
            )
            
            CookieServices().set(custom_response, response.data["refresh"])
            
            return custom_response

        except AuthenticationFailed:
            return Response(
                data={"error": "Неверный email или пароль"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            settings.ERROR_LOGGER.error(
                f"Authentication error: {str(e)}",
                exc_info=True,
                extra={"email": request.data.get("email")}
            )
            return Response(
                data={"error": "Произошла ошибка при авторизации"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RefreshAPIView(APIView):
    """
    API для обновления JWT токенов.
    Принимает refresh-токен и возвращает новый access-токен.
    """
    
    @swagger_auto_schema(
        operation_summary="Обновление access-токена",
        operation_description="""
        Обновляет JWT access-токен с помощью валидного refresh-токена.
        
        Требования:
        - Действительный refresh-токен в cookie
        - Токен не должен быть в blacklist
        
        Возвращает:
        - Новый access-токен в теле ответа
        """,
        tags=["Пользователь"],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Успешное обновление токена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Новый access токен'
                        ),
                    },
                    example={
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Ошибка генерации JWT access-токена",
                examples={
                    "application/json": {
                        "error": "Refresh токен отсутствует / Токен больше недействителен / Невалидный токен"
                    }
                }
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Внутренняя ошибка сервера",
                examples={
                    "application/json": {
                        "error": "Произошла ошибка при обновлении токена"
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Обрабатывает запрос на обновление токена.
        """
        cookie_service = CookieServices()

        try:
            refresh_token = cookie_service.get(request)
            if not refresh_token:
                raise AuthenticationFailed("Refresh токен отсутствует")

            token = RefreshToken(refresh_token)
            try:
                token.check_blacklist()
            except TokenError:
                raise AuthenticationFailed("Токен больше недействителен")
            
            new_access = str(token.access_token)

            return Response(
                data={"access": new_access},
                status=status.HTTP_200_OK
            )
        except AuthenticationFailed as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except TokenError as e:
            return Response(
                {"error": "Невалидный токен"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            settings.ERROR_LOGGER.error(
                f"Refresh error: {str(e)}", 
                exc_info=True,
                extra={"user": request.user.id if request.user.is_authenticated else None}
            )
            return Response(
                {"error": "Произошла ошибка при обновлении токена"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RegisterAPIView(APIView):
    """
    API для регистрации новых пользователей.
    """

    @swagger_auto_schema(
        operation_summary="Регистрация новых пользователей",
        operation_description="Создает нового пользователя в системе. " \
        "При успешной регистрации возвращает JWT access-токен и устанавливает refresh-токен в cookie.",
        request_body=RegisterUserSerializer,
        tags=["Пользователь"],
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Успешная регистрация",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='JWT access token'
                        )
                    }
                ),
                examples={
                    "application/json": {
                        "access": "token"
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Невалидные данные",
                examples={
                    "application/json": {
                        "error": {
                            "email": ["Это поле обязательно."],
                            "password": ["Пароль слишком простой."]
                        }
                    }
                }
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Внутренняя ошибка сервера",
                examples={
                    "application/json": {
                        "error": "Произошла ошибка при регистрации"
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                data={"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = serializer.save()
            
            tokens = TokenObtainPairSerializer.get_tokens(user)
            response = Response(
                data={"access": tokens["access"]},
                status=status.HTTP_201_CREATED
            )

            CookieServices().set(response, tokens["refresh"])
            return response

        except Exception as ex:
            settings.ERROR_LOGGER.error(f"Registration error: {str(ex)}", exc_info=True)
            return Response(
                data={"error": "Произошла ошибка при регистрации"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class LogoutAPIView(APIView):
    """
    API для выхода пользователя из системы.
    Удаляет JWT refresh-токен из HTTP-only cookie.
    """

    @swagger_auto_schema(
        operation_summary="Выход из системы",
        operation_description="Удаляет refresh-токен из cookies.",
        tags=["Пользователь"],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="Взятие JWT refresh-токена из Cookie и занесение его в blacklist",
                examples={
                    "application/json": {
                        "detail": "Успешный выход из системы"
                    }
                }
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Внутренняя ошибка сервера",
                examples={
                    "application/json": {
                        "error": "Произошла ошибка при выходе из системы"
                    }
                }
            )
        }
    )
    def post(self, request):
        """
        Обрабатывает запрос на выход из системы.
        Удаляет refresh-токен из cookies и делает его недействительным.
        """
        try:
            cookie_service = CookieServices()

            refresh_token = cookie_service.get(request)
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()   # Добавляем токен в blacklist
                cookie_service.delete(request)
            
            response = Response(
                data={"detail": "Успешный выход из системы"},
                status=status.HTTP_204_NO_CONTENT
            )
            return response
        except TokenError:
            return Response(
                data={"detail": "Успешный выход из системы"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as ex:
            settings.ERROR_LOGGER.error(
                f"Logout error: {str(ex)}", 
                exc_info=True, 
                extra={"user": request.user.id if request.user.is_authenticated else None}
            )
            return Response(
                {"error": "Произошла ошибка при выходе из системы"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserAPIView(APIView):
    """
    API для работы с модель User.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получить информацию о пользователе",
        operation_description="Предоставляет информацию авторизированного пользователя",
        tags=["Пользователь"],
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description='Bearer токен. Пример: "Bearer eyJhbGciOi..."',
                default="Bearer "
            )
        ],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Внутренняя ошибка сервера",
                examples={
                    "application/json": {
                        "error": "Произошла ошибка при получении инфомарции"
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            serializer = UserSerializer(request.user)

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as ex:
            settings.ERROR_LOGGER.error(f"Get info user data error: {str(ex)}", exc_info=True)
            return Response(
                data={"error": "Произошла ошибка при получении инфомарции"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        