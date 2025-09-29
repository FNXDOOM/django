# alerts/urls.py
from django.urls import path
from .views import CreateAlertView

urlpatterns = [
    path('create/', CreateAlertView.as_view(), name='create-alert'),
]