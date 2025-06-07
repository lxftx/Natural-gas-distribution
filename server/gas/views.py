from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from gas.models import History
from gas.serializers import (CalculatedSerializer, CalculateSerializer,
                             CreateHistorySerializer, GetHistorySerializer)
from gas.services import DefaultInputValues, GasDistributionService
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class CalculateAPIView(APIView):
    """
    API метод расчета задачи распределения природного газа в группе доменных печей.
    """
    
    @swagger_auto_schema(
        operation_summary="Вызов расчета природного газа",
        operation_description="API метод расчета задачи распределения природного газа в группе доменных печей",
        request_body=CalculateSerializer,
        tags=["Расчет"],
        responses={
            status.HTTP_200_OK: CalculatedSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Оптимальное решение не найдено",
                examples={
                    "application/json": {
                        "error": "<Ошибка>"
                    }
                }
            )
        }
    )
    def post(self, request):
        try:
            serializer = CalculateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            result = GasDistributionService.calculate_distribution(serializer.validated_data)
            serializer = CalculatedSerializer(data=result)
            serializer.is_valid(raise_exception=True)

            result = serializer.validated_data
            return Response(
                data=result,
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                data={"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class DefaultInputValuesAPIView(APIView):
    """
    API метод получения входных значений по умолчанию
    """

    @swagger_auto_schema(
        operation_summary="Получить значения по умолчанию",
        operation_description="API метод получения входных значений по умолчанию",
        tags=["Значения по умолчанию"],
        responses={
            status.HTTP_200_OK: CalculateSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Ошибка получения входных данных",
                examples={
                    "application/json": {
                        "error": "<Ошибка>"
                    }
                }
            )
        }
    )
    def get(self, *args, **kwargs):
        try:
            values = DefaultInputValues.get_default_values()
            serializer = CalculateSerializer(data=values)
            serializer.is_valid(raise_exception=True)

            result = serializer.validated_data
            return Response(
                data=result,
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                data={"error": "Ошибка при получений входных значений по умолчанию."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
class HistoryAPIView(APIView):
    """
    API endpoint для работы с историей расчета.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Список всех записей истории",
        operation_description="Возвращает список всех записей истории для аутентифицированного пользователя",
        tags=['История расчетов'],
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description='Bearer токен. Пример: "Bearer eyJhbGciOi..."',
                default="Bearer "
            ),
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description='ID конкретной истории',

            )
        ],
        responses={
            status.HTTP_200_OK: GetHistorySerializer(many=True),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="История не была найдена",
                examples={
                    "application/json": {
                        "error": "История не найдена"
                    }
                }
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Внутренняя ошибка сервера",
                examples={
                    "application/json": {
                        "error": "Произошла ошибка при получении истории/историй"
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            history_id = request.query_params.get("id")
            if history_id:
                history = History.objects.filter(id=history_id, user=request.user).select_related("calculate", "user").first()

                if not history:
                    raise NotFound("История не найдена")
                
                serializer = GetHistorySerializer(history)
            else:
                queryset = History.objects.filter(user=request.user).select_related("calculate", "user")
                serializer = GetHistorySerializer(queryset, many=True)


            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except NotFound as e:
            return Response(
                data={"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            settings.ERROR_LOGGER.error(f"HistoryAPI GET error: {str(e)}", exc_info=True)
            return Response(
                {"error": "Ошибка при получении истории расчетов"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        

    @swagger_auto_schema(
        operation_summary="Создание новой записи истории",
        operation_description="Создает новую запись в истории расчетов",
        tags=['История расчетов'],
        request_body=CreateHistorySerializer,
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
            status.HTTP_201_CREATED: openapi.Response(
                description="История расчетов создана",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Внутренняя ошибка сервера",
                examples={
                    "application/json": {
                        "error": "Произошла ошибка при сохранении истории"
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateHistorySerializer(data=request.data, context={"request": request})
        try:
            if not serializer.is_valid():
                return Response(
                    data={"error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save()
            return Response(
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            settings.ERROR_LOGGER.error(f"HistoryAPI POST error: {str(e)}", exc_info=True)
            return Response(
                {"error": "Произошла ошибка при сохранении истории"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        
        
    @swagger_auto_schema(
        operation_summary="Удаление записи истории",
        operation_description="Удаляет конкретную запись из истории расчетов",
        tags=['История расчетов'],
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description='Bearer токен. Пример: "Bearer eyJhbGciOi..."',
                default="Bearer "
            ),
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="Идентификатор истории для удаления истории"
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="История удалена"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="История не была найдена",
                examples={
                    "application/json": {
                        "error": "История не найдена"
                    }
                }
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Внутренняя ошибка сервера",
                examples={
                    "application/json": {
                        "error": "Произошла ошибка при удалении истории"
                    }
                }
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            history_id = request.query_params.get("id")

            History.objects.get(id=history_id).delete()

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except History.DoesNotExist:
            return Response(
                data={"error": "История не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            settings.ERROR_LOGGER.error(f"HistoryAPI POST error: {str(e)}", exc_info=True)
            return Response(
                {"error": "Произошла ошибка при удалении истории"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )   