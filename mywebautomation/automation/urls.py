from django.urls import path # type: ignore
from .views import CommandView
from . import views


urlpatterns = [
    path('api/command/', CommandView.as_view(), name='command'),
    path('execute_puppeteer/', views.execute_puppeteer_script, name='execute_puppeteer'),
]
