from unicodedata import name
from django.urls import path
from .views import createShortUrl, shortUrlView, getMyUrls, testIP

urlpatterns = [
    path('test/', createShortUrl, name='test'),
    path('test/<str:pk>/', shortUrlView.as_view(), name='view'),
    path('test/all', getMyUrls, name='my-urls'),
    path('test/test', testIP, name='testIP')
]
