from django.urls import path
from .views import ProductAPI,CategoryAPI
from django.shortcuts import render

# frontend page
def home_page(request):
    return render(request, "home.html")


    
urlpatterns = [
    path('', home_page),
    # API routes
    path('products/', ProductAPI.as_view(),name='products'),
    path('products/<int:id>/', ProductAPI.as_view(),name='product-detail'),
      # 👇 Category routes
    path('categories/', CategoryAPI.as_view()),
    path('categories/<int:id>/', CategoryAPI.as_view()),

]