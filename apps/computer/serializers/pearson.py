from rest_framework import serializers

from apps.computer.models import DataModel, PCorrelationModel


class DataPointSerializer(serializers.Serializer):
    date = serializers.DateField(allow_null=False)
    value = serializers.FloatField(allow_null=True)


class CorrelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCorrelationModel
        exclude = ('data', )


class DataSerializer(serializers.ModelSerializer):
    x = DataPointSerializer(many=True, write_only=True)
    y = DataPointSerializer(many=True, write_only=True)
    correlations = CorrelationSerializer(many=True, read_only=True)

    class Meta:
        model = DataModel
        fields = '__all__'
        read_only_fields = ('user', )


class PCorrelationRequestSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(allow_null=False)
    data = DataSerializer(allow_null=False, write_only=True)