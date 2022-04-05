from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.serializers import urlSerializer
from rest_framework import status
from .models import url
import simpleUID
from django.shortcuts import redirect
from rest_framework import generics
from .permissions import ReadOnly
import ipinfo
import os


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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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

            handler = ipinfo.getHandler(os.environ.get('IP_ACCESS_TOKEN'))
            details = handler.getDetails(request.META.get('REMOTE_ADDR'))
            data = {
                'country': details.country,
                'city': details.city
            }
            print(request.META.get('REMOTE_ADDR'))
            print(data)
            return redirect(u.long_url)
        except url.DoesNotExist:
            return Response({"message": "The link you are trying to reach does not exist"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyUrls(request):

    try:
        u = url.objects.filter(owner=request.user.id)
        urls = urlSerializer(u, many=True).data
        return Response({"message": urls})
    except url.DoesNotExist:
        return Response({"message": "you do not have any short urls"})


@api_view(['GET'])
def testIP(request):
    handler = ipinfo.getHandler(os.environ.get('IP_ACCESS_TOKEN'))
    details = handler.getDetails(request.META.get('REMOTE_ADDR'))
    data = {
        'country': details.country,
        'city': details.city,
        'ip': request.META.get('REMOTE_ADDR')
    }
    return Response({"message": data})
