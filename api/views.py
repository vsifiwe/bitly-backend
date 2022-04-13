import csv
import re
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.serializers import DeviceSerializer, urlSerializer
from rest_framework import status
from .models import Device, url
import simpleUID
from django.shortcuts import redirect
from rest_framework import generics
from .permissions import ReadOnly
import ipinfo
import os
from .helpers import deviceType, decode_utf8


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createShortUrl(request):
    data = {
        'long_url': request.data['url'],
        'uuid': simpleUID.string(),
        'impressions': 0,
        'owner': request.user.id
    }

    # check if url is valid

    # create a url instance
    serializer = urlSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        data['shortUrl'] = os.environ.get("SHORT_BASE_URL") + data['uuid']
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class shortUrlView(generics.RetrieveUpdateAPIView):
    queryset = url.objects.all()
    serializer_class = urlSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def retrieve(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            u = url.objects.get(uuid=pk)

            # increment impressions
            impressions = u.impressions + 1
            u.impressions = impressions
            u.save()

            if 'HTTP_X_FORWARDED_FOR' in request.META:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                ip = x_forwarded_for.split(',')[0]
            else:
                # ip = request.META.get('REMOTE_ADDR')
                ip = '196.12.140.219'

            # Documentation: https: // github.com/ipinfo/python
            # Get Token from https: // ipinfo.io/account/home
            handler = ipinfo.getHandler(os.environ.get('IP_ACCESS_TOKEN'))
            details = handler.getDetails(ip)
            dev = deviceType(request)
            data = {
                'url': u.id,
                'country': details.country,
                'city': details.city,
                'ip': ip,
                'os': dev['os'],
                'browser': dev['browser']
            }
            d = DeviceSerializer(data=data)
            if d.is_valid():
                d.save()
            return redirect(u.long_url)
        except url.DoesNotExist:
            return Response({"message": "The link you are trying to reach does not exist"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyUrls(request):

    try:
        u = url.objects.filter(owner=request.user.id)
        urls = urlSerializer(u, many=True).data
        devInfo = []
        views = 0
        for x in urls:
            x['shortUrl'] = os.environ.get("SHORT_BASE_URL") + x['uuid']
            d = Device.objects.filter(url=x['id'])
            data = DeviceSerializer(d, many=True).data
            x['data'] = data
            for y in data:
                devInfo.append(y)
            views = views + x['impressions']
        return Response({"shorturls": urls, "totalViews": views, "deviceInfo": devInfo})
    except url.DoesNotExist:
        return Response({"message": "you do not have any short urls"})


@api_view(['GET'])
def testIP(request):

    if 'HTTP_X_FORWARDED_FOR' in request.META:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    handler = ipinfo.getHandler(os.environ.get('IP_ACCESS_TOKEN'))
    details = handler.getDetails(ip)
    dev = deviceType(request)
    data = {
        'country': details.country,
        'city': details.city,
        'ip': ip,
        'os': dev['os'],
        'browser': dev['browser']
    }
    print(data)
    return Response({"message": data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulkShorten(request):
    file = request.FILES['csv_file']
    csv_file = csv.DictReader(decode_utf8(file))
    try:
        for row in csv_file:
            data = {
                'long_url': row['Link'],
                'uuid': simpleUID.string(),
                'impressions': 0,
                'owner': request.user.id
            }

            # check if url is valid

            # create a url instance
            serializer = urlSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
    except:
        return Response({"message": "error"})

    return Response({"message": "success"})
