from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('', views.crm_dashboard, name='dashboard'),
    path('clients/', views.client_list, name='client_list'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path('create-order/', views.create_order, name='create_order'),
]