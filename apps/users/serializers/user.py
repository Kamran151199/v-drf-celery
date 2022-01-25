from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'profile',
            'phone_number',
            'is_lecturer',
            'is_active',
            'is_staff',
            'is_verified',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ('is_active', 'is_staff', 'profile', 'is_verified', 'id', 'profile')

    def get_fields(self, *args, **kwargs):
        fields = super(UserSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) in ["PATCH"]:
            fields['email'].required = False
            fields['username'].required = False
        return fields