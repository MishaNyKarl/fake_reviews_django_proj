from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.offer_detail, name='offer_detail'),
]