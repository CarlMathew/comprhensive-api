from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from .models import Product
from .serializer import ProductSerializer
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from Users import permissions
from rest_framework.permissions import IsAuthenticated
# from django.db.models import Q
# from django.shortcuts import get_list_or_404

# Create your views here.


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListAPIView(generics.ListAPIView):
    """
        Fetch all of the data from Products
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.isUser, IsAuthenticated]

class ProductStockListAPIView(generics.ListAPIView):
    """
        Filter products by stock quantity greater than a specified value
    """
    serializer_class = ProductSerializer
    

    def get_queryset(self):
        gt_parameters = self.request.query_params.get("gt")
        if not gt_parameters:
            raise ValueError({"error": "Value Error: Please provide the greater than (gt) parameters"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            quantity = float(gt_parameters)
            if quantity < 0:
                raise ValueError("Negative Number is not allowed")
            return Product.objects.filter(quantity_in_stock__gt = quantity)
        except ValueError:
            raise ValueError("The gt must be a valid number")


class ProductCreateAPIView(generics.CreateAPIView):
    """
        Handles and Create new Products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(generics.UpdateAPIView):
    """
        Update product by its name
    """

    qeuryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "name"

    def get_object(self):
        name = self.request.query_params.get("name")
        if not name:
            raise ValueError("Please provide a 'name' parameter.")
        return get_object_or_404(Product, name = name)
        # return get_object_or_404(Product, name = name, type = type) #AND Operator
        # return get_list_or_404(Product, Q(name = name) | Q(type = product_type) ) #OR Operator

class ProductIDUpdateAPIView(generics.UpdateAPIView):
    """
        Update product by its product_id
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "product_id"


    def get_object(self):
        product_id = self.request.query_params.get("product_id")
        if not product_id:
            raise ValueError("Please provide the product_id")
        return get_object_or_404(Product, product_id = product_id)


class ChangeQuantityAPIView(APIView):
    """
        This will change increment and decrement the quantity_in_stock
        Params:
            action = 0 for decrement and 1 for increment
            type = type of product
         Body:
            quantity = how much quantity
    """

    def put(self, request, *args, **kwargs):
        action = int(request.query_params.get("action"))
        type = request.query_params.get("type")

        if action not in [0, 1]:
            raise ValueError("Please only provide 1 and 2")
        if not isinstance(type, str):
            raise ValueError("Only Return String Value")

        try:
            quantity = int(request.data.get("quantity"))
            if quantity < 0:
                raise ValueError("Please only provide a positive numbers")
            with connection.cursor() as cursor:
                
                cursor.execute("CALL addQuantity(%s, %s, %s)", [action, str(type), quantity])

                updated_products = Product.objects.filter(type = type)
                serializer = ProductSerializer(updated_products, many = True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e: 
            return Response({"error": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDestoyAPIView(generics.DestroyAPIView):
    """
        Deletes a product by its ID

    """

    serializer_class = ProductSerializer
    lookup_field = "product_id"


    def delete(self, request, *args, **kwargs):
        product_id = self.request.query_params.get("product_id")
        if not product_id:
            raise ValueError({"error": "Please make sure to provide product id"})
        instance = get_object_or_404(Product, product_id = product_id)
        instance.delete()
        remaining_products = Product.objects.all()
        serializer = ProductSerializer(remaining_products, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        




