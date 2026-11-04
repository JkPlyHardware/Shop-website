from rest_framework import serializers
class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500, trim_whitespace=True)
    history = serializers.ListField(child=serializers.DictField(), required=False, max_length=6)
    def validate_message(self, value):
        if not value.strip(): raise serializers.ValidationError("Message cannot be empty.")
        return value.strip()
