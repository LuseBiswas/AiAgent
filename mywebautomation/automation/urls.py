from django.urls import path # type: ignore
from .views import CommandView

urlpatterns = [
    path('api/command/', CommandView.as_view(), name='command'),
]
