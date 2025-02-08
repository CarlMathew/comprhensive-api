from .models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "product_id",
            "name",
            "quantity_in_stock",
            "unit_price",
            "type"
        ]
        read_only_fields = ["product_id"]

    def validate_quantity_in_stock(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Make sure it is an integer.")
        if value < 0:
            raise serializers.ValidationError("Negative numbers are not accepted.")
        return value  # Ensure the value is returned

    def validate_unit_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Please provide a positive number.")
        return value  # Ensure the value is returned
