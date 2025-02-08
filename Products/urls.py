from django.urls import path
from . import views

urlpatterns = [
    path("all/", view=views.ProductListAPIView.as_view()),
    path('quantity/gt/', view = views.ProductStockListAPIView.as_view()),
    path('product/add/', view = views.ProductCreateAPIView.as_view()),
    path("product/update/", view = views.ProductUpdateAPIView.as_view()),
    path("product/update/quantity", view=views.ChangeQuantityAPIView.as_view()),
    path("product/delete/", view=views.ProductDestoyAPIView.as_view())
]



