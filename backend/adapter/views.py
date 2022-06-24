import os
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, ListAPIView

from .models import Image, Profile, Token
from .serializer import ImageSubmitSerializer, ImageSerializer, ImageCreateBinarySerializer


class ImageCreateAPIView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSubmitSerializer

    # TODO anonymous user
    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(profile=profile)


class ImageListAPIView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return Image.objects.none()
        profile = Profile.objects.get(user=user)
        return qs.filter(profile=profile)


class BinaryImageUrl(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageCreateBinarySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["expiration_time"] = self.kwargs['expiration_time']
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return Image.objects.none()
        profile = Profile.objects.get(user=user)
        return qs.filter(profile=profile)


@api_view(['GET'])
def binary_image(request, token, image_name):
    get_object_or_404(Token, token=token, expiration__gte=datetime.now())
    valid_image = f'/media/binary/{image_name}'
    return redirect(valid_image)
