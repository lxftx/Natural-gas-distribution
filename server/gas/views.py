from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from gas.serializers import CalculateSerializer
from gas.services import GasDistributionService
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
            status.HTTP_200_OK: openapi.Response(
                description="Оптимальное решение найдено",
                examples={
                    "application/json": {
                        "objective": 123.123,
                        "gas_distribution": [10.00, 20.00, 30.00, 40.00],
                        "total_gas_consumption": 123.123,
                        "total_coke_consumption": 123.123,
                        "total_iron_production": 123.123,
                        "sulfur_content": [10.00, 20.00, 30.00, 40.00],
                        "status": "OPTIMAL"
                    }
                }
            ),
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
            return Response(
                data=result,
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                data={"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )