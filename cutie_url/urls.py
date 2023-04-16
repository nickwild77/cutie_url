from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api.views import URLCreateView, URLRedirectView, HomeView, URLListView

app_name = 'api'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/', URLCreateView.as_view(), name='url_create'),
    path('list/', URLListView.as_view(), name='list'),
    path('<str:short_url>/', URLRedirectView.as_view(), name='url_redirect'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
