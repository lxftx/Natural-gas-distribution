from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from gas.serializers import CalculateSerializer, CalculatedSerializer
from gas.services import GasDistributionService
from gas.services import DefaultInputValues
from rest_framework import status
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