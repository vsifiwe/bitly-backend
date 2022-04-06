from unicodedata import name
from django.urls import path
from .views import createShortUrl, shortUrlView, getMyUrls, testIP

urlpatterns = [
    path('create/', createShortUrl, name='test'),
    path('<str:pk>/', shortUrlView.as_view(), name='view'),
    path('urls', getMyUrls, name='my-urls'),
    path('test/test', testIP, name='testIP')
]
