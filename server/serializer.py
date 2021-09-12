from rest_framework import serializers

from server.models import stocks


class stocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = stocks
        fields = '__all__'