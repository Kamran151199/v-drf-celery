from abc import ABC
from rest_framework import serializers


class DataPointSerializer(serializers.Serializer, ABC):
    date = serializers.DateField(allow_null=False)
    value = serializers.FloatField(allow_null=True)


class DataSerializer(serializers.Serializer, ABC):
    x_data_type = serializers.CharField(max_length=200)
    y_data_type = serializers.CharField(max_length=200)
    x = DataPointSerializer(many=True)
    y = DataPointSerializer(many=True)


class PCorrelationRequestSerializer(serializers.Serializer, ABC):
    user_id = serializers.UUIDField(allow_null=False)
    data = DataSerializer(allow_null=False)

