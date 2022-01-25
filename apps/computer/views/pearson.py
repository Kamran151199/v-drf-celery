from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.computer.serializers.pearson import PCorrelationRequestSerializer
from apps.computer.tasks.pearson import compute_pcorrelation


@api_view(['POST'])
def post_data(request):
    """
    Post the data for p-correlation computation.
    """

    serializer = PCorrelationRequestSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        compute_pcorrelation.delay(data=data)
        return Response(status=status.HTTP_201_CREATED)


