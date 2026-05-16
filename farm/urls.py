from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('order/', views.order_assistant, name='order_assistant'),
    path('order/success/<str:reference>/', views.order_success, name='order_success'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/orders/', views.dashboard_orders, name='dashboard_orders'),
    path('dashboard/orders/<int:pk>/', views.dashboard_order_detail, name='dashboard_order_detail'),
    path('dashboard/products/', views.dashboard_products, name='dashboard_products'),
    path('dashboard/products/create/', views.dashboard_product_create, name='dashboard_product_create'),
    path('dashboard/products/<int:pk>/edit/', views.dashboard_product_edit, name='dashboard_product_edit'),
]
