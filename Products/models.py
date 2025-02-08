from django.db import models


# Create your models here.

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null = True, blank=True)
    quantity_in_stock = models.IntegerField(default=0)
    unit_price = models.DecimalField(default=2.00, decimal_places=2, max_digits=18)
    type = models.CharField(max_length = 255, null = True , blank = True)

    @property
    def total_revenue(self):
        return self.quantity_in_stock * self.unit_price
    
    def __repr__(self):
        return f"Product Name: {self.name}, Quantity: {self.quantity_in_stock}"
    
    class Meta:
        db_table = "products"
        managed = False