from django.db import transaction
from rest_framework import viewsets, generics, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Image, Profile
from .serializer import ProfileSerializer, ImageSerializer

from django.http import HttpResponse


class AttachmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(profile=profile)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if not user.is_authenticated:
            return Image.objects.none()
        # print(request.user)
        profile = Profile.objects.get(user=user)
        return qs.filter(profile=profile)
