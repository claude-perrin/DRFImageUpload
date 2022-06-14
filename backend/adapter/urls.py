from django.urls import path
from django.views.generic import TemplateView

from .views import  AttachmentListCreateAPIView, AttachmentDetailAPIView




urlpatterns = [
    path('', AttachmentListCreateAPIView.as_view()),
    path('<int:pk>/', AttachmentDetailAPIView.as_view())
]


