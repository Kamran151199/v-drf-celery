from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.users.models import User
from apps.users.serializers.user import UserSerializer
from apps.users.signals import send_verification_email
from helpers.permissions.identity import IsSelfOrIsAuth


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsSelfOrIsAuth)

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    filterset_fields = ('email', 'username', 'first_name', 'last_name')

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        if self.action in ['create', 'verify_token']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsSelfOrIsAuth]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        send_verification_email.send(sender=User, user=user)
        return Response(data=self.get_serializer(user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary='Email verification',
                         operation_description='Verify registration token sent to email',
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['verification-token'],
                             properties={'verification-token': openapi.Schema(type=openapi.TYPE_STRING)},
                         ), methods=['POST'])
    @action(methods=['POST'], detail=True, permission_classes=(AllowAny,), url_path='verify', url_name='verify')
    def verify_token(self, request, pk, *args, **kwargs):
        verification_code = request.data.get('verification-token')
        token = JWTAuthentication().get_validated_token(verification_code)
        user = JWTAuthentication().get_user(token)
        if user:
            if str(user.id) not in [pk]:
                raise ValidationError(detail='Sorry, this token does not belong to you!')
            user.verify()
        return Response(data=self.get_serializer(user).data, status=status.HTTP_200_OK)
