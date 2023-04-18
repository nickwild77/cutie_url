import hashlib

from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import URL
from .serializers import URLSerializer
import redis

r = redis.Redis(host='localhost', port=6379, db=0)


class URLViewSet(ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def create(self, request, *args, **kwargs):
        # Get the long URL from the request data
        long_url = request.data.get('long_url')

        # Check if the long URL is already cached in Redis
        short_url = r.get(long_url)

        if not short_url:
            # Generate the short URL using MD5 algorithm
            hash_object = hashlib.md5(long_url.encode())
            short_url = hash_object.hexdigest()[:8]

            # Cache the long URL and the corresponding short URL in Redis
            r.set(long_url, short_url)
            r.set(short_url, long_url)

            # Create a new URL object with the short URL and long URL
            url = URL.objects.create(short_url=short_url, long_url=long_url)

            # Serialize the URL object and return the response
            serializer = URLSerializer(url)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Retrieve the URL object from the short URL and serialize it
            url = URL.objects.get(short_url=short_url.decode())
            serializer = URLSerializer(url)
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        url = self.get_object()
        url.clicked()
        return Response(status=status.HTTP_302_FOUND, headers={'Location': url.long_url})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = URLSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
