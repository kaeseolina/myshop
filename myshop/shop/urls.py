from django.urls import path, re_path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),  # URL для всех продуктов
    path('category/<slug:category_slug>/', views.category_view, name='category_detail'),  # URL для категорий
    path('<slug:category_slug>/', views.product_list_by_category, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.category_view, name='category'),
]
