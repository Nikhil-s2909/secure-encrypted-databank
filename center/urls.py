from django.urls import path
from . import views

urlpatterns = [
    path('center_login/', views.center_login),
    path('center_register/', views.center_register),
    path('center_user/', views.center_user),
    path('center_logout/', views.center_logout),
    path('upload/', views.upload_file),
    path('my_files/', views.my_files),
    path('download/<int:file_id>/', views.decrypt_and_download),
]
