from django.urls import path
from . import views

urlpatterns = [
    path('center_login/', views.center_login),
]
