from django.urls import path
from .views import createShortUrl, viewShortUrl, shortUrlView

urlpatterns = [
    path('test/', createShortUrl, name='test'),
    path('test/<str:pk>/', shortUrlView.as_view(), name='view'),
]
