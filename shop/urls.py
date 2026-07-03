from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.ProductFilterView.as_view(), name='products'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product'),
    path('product/<slug:slug>/review/', views.add_review, name='add_review'),
    path('search/', views.search, name='search'),
]
