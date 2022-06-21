from django.urls import path
from django.views.generic import TemplateView

from .views import AttachmentListCreateAPIView


#
#
urlpatterns = [
    path('', AttachmentListCreateAPIView.as_view()),
]
#
#
