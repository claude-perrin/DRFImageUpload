from django.urls import path

from .views import ImageListAPIView, ImageCreateAPIView, BinaryImageUrl, binary_image

# "http://localhost:8000/view/binary/b72e0067c5d74d1e1cc943c72b7f1bc12dcaf468/BINARY-sL3.jpg"

urlpatterns = [
    path('view', ImageListAPIView.as_view()),
    path('view/binary/<int:expiration_time>', BinaryImageUrl.as_view()),
    path('view/binary/<str:token>/<str:image_name>', binary_image),

    path('create', ImageCreateAPIView.as_view()),
]
