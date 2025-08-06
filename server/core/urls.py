from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('text_to_image/', views.text_to_image, name='text_to_image'),
    path('chat/', views.chat, name='chat'),
    
    
]
