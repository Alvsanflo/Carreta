from django.urls import path
from . import views

urlpatterns = [
    path('', views.persona_list, name='persona_list'),
    path('crear/', views.persona_form, name='persona_create'),
    path('<int:pk>/', views.persona_detail, name='persona_detail'),
    path('<int:pk>/editar/', views.persona_form, name='persona_edit'),
    path('analytics/', views.analytics, name='analytics'),
    path('shopping-list/', views.shopping_list, name='shopping_list'),
    path('shopping-list/pdf/', views.shopping_list_pdf, name='shopping_list_pdf'),
    path('stock/', views.stock_view, name='stock'),
]
