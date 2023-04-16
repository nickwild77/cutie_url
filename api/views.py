import hashlib

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import URL
from .serializers import URLSerializer
import redis

r = redis.Redis(host='localhost', port=6379, db=0)


class HomeView(TemplateView):
    template_name = 'home.html'


class URLCreateView(CreateAPIView):
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


class URLRedirectView(APIView):
    @staticmethod
    def get(request, short_url):
        url = get_object_or_404(URL, short_url=short_url)
        url.clicked()
        return Response({'url': url.long_url}, status=status.HTTP_302_FOUND)


class URLListView(APIView):
    @staticmethod
    def get(request):
        urls = URL.objects.all()
        serializer = URLSerializer(urls, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
