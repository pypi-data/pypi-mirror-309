from rest_framework import serializers
from google.protobuf.json_format import MessageToDict
from google._upb._message import RepeatedCompositeContainer


class ProtoSerializer(serializers.Serializer):
    """
    Base serializer for handling protobuf data.
    """

    def __init__(self, instance=None, data=None, **kwargs):
        if instance is not None:
            instance = self.to_representation(instance)
        super().__init__(instance=instance, data=data, **kwargs)

    def to_representation(self, instance):
        """
        Converts protobuf to dict.
        """
        if isinstance(instance, RepeatedCompositeContainer):
            return [MessageToDict(obj, preserving_proto_field_name=True) for obj in instance]
        elif isinstance(instance, list):
            return [MessageToDict(obj, preserving_proto_field_name=True) for obj in instance]
        data = MessageToDict(instance, preserving_proto_field_name=True)
        return self.filter_fields(data)

    def filter_fields(self, data):
        """
        Filters data based on fields defined in the serializer.
        """
        allowed_fields = set(self.fields.keys())
        return {key: value for key, value in data.items() if key in allowed_fields}

    def create(self, validated_data):
        """
        Creates a protobuf instance based on the data.
        """
        proto_class = self.Meta.proto_class
        return proto_class(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates an existing protobuf instance.
        """
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
