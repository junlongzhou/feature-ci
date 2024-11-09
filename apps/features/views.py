from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from features.models import Feature, Component, Build
from features.serializers import FeatureSerializer, ComponentSerializer, BuildSerializer, \
    FeaturePrettySerializer, FeatureCommandSerializer
from features.filtersets import ComponentFilter

@api_view(['POST'])
@permission_classes([AllowAny])
def user_auth(request, **kwargs):
    user = authenticate(username=request.data.get("username", ""),
                        password=request.data.get("password", ""))
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"username": user.get_username(),
                         "id": user.pk,
                         "email": user.email,
                         "token": token.key, "created": created})
    return Response({"username": request.data.get("username", ""), "token": ""})


class FeatureList(generics.ListCreateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('name', 'status',)

class FeatureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    def retrieve(self, request, *args, **kwargs):
        if request.query_params and 'pretty' in request.query_params:
            return Response(FeaturePrettySerializer(self.get_object()).data)
        return super().retrieve(request, *args, **kwargs)

class ComponentList(generics.ListCreateAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComponentFilter

class ComponentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class BuildList(generics.ListCreateAPIView):
    queryset = Build.objects.all()
    serializer_class = BuildSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('name', 'status',)

class BuildDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Build.objects.all()
    serializer_class = BuildSerializer

class FeatureCommand(generics.CreateAPIView):
    serializer_class = FeatureCommandSerializer

    def post(self, request, *args, **kwargs):
        request.data.update({'feature_id': int(kwargs.pop('feature_id'))})
        return super().post(request, *args, **kwargs)
