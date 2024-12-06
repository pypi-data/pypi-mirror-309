from rest_framework import serializers
from google.protobuf.json_format import MessageToDict
from google._upb._message import RepeatedCompositeContainer


class ProtoSerializer(serializers.Serializer):
    """
    Generic serializer for converting protobuf messages to JSON serializable objects.
    """

    def __init__(self, instance=None, data=None, **kwargs):
        if instance is not None:
            # Konwertujemy protobuf na dict tylko gdy mamy instance
            data = self.to_representation(instance)
            kwargs['data'] = data
            instance = None
        super().__init__(instance=instance, **kwargs)
        if data is not None:
            self.is_valid()

    def to_representation(self, instance):
        """
        Converts protobuf to dict, handling both single instances and lists/repeated fields.
        """
        if isinstance(instance, (RepeatedCompositeContainer, list)):
            return [MessageToDict(obj, preserving_proto_field_name=True) for obj in instance]
        return MessageToDict(instance, preserving_proto_field_name=True)
