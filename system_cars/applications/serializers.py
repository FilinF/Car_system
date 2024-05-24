from rest_framework import serializers
from rest_enumfield import EnumField
from .models import CarEntryStatus



class CarEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = EnumField(CarEntryStatus, required = False)
    coordinate_x = serializers.IntegerField()
    coordinate_y = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    s_location = serializers.ListField()
    f_location = serializers.ListField()


class IDSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class CreateRouteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    coordinate_x = serializers.IntegerField()
    coordinate_y = serializers.IntegerField()

class OperationSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    done = serializers.BooleanField(read_only=True)
    result = serializers.DictField(read_only=True, allow_null=True)