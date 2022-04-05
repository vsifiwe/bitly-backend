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
            return redirect(u.long_url)
        except url.DoesNotExist:
            return Response({"message": "The link you are trying to reach does not exist"})
