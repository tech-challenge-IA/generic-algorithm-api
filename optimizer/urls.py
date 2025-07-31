from django.urls import path
from .views import OtimizacaoAPIView

urlpatterns = [
    path('otimizar/', OtimizacaoAPIView.as_view(), name='otimizar'),
]
