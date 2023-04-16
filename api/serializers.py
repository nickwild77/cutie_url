from rest_framework.serializers import ModelSerializer
from .models import URL


class URLSerializer(ModelSerializer):
    class Meta:
        model = URL
        fields = ('id', 'long_url', 'short_url', 'created_at')
