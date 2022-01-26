from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.computer.models import DataModel
from apps.computer.serializers.pearson import PCorrelationRequestSerializer, DataSerializer
from apps.computer.tasks.pearson import compute_pcorrelation
from apps.users.models import User


class CorrelationViewSet(viewsets.GenericViewSet, ListModelMixin,
                         RetrieveModelMixin, DestroyModelMixin):
    queryset = DataModel.objects.all()
    serializer_class = DataSerializer
    permission_classes = (IsAuthenticated, )

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ('x_data_type', 'y_data_type')
    filterset_fields = ('x_data_type', 'y_data_type', 'user_id')

    @swagger_auto_schema(operation_summary='Pearson Computation',
                         operation_description='Computes the correlative of the provided data vectors',
                         request_body=PCorrelationRequestSerializer, methods=['POST'])
    @action(methods=['POST'], detail=False, serializer_class=PCorrelationRequestSerializer,
            permission_classes=(IsAuthenticated,), url_name='compute')
    def compute(self, request, *args, **kwargs):
        """
        Post the data for p-correlation computation.
        """

        serializer = PCorrelationRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            user = User.objects.filter(
                id=data.get('user_id')).first()  # Could use get_object_or_404, but want a custom error message :-)
            if not user:
                raise ValidationError(detail='Provided user does not exist.')
            compute_pcorrelation.delay(data=data)
            return Response(status=status.HTTP_201_CREATED)
