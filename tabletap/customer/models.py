from django.db import models
from restaurant.models import Table, MenuItem

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=50)  # pending, preparing, completed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - Table {self.table.table_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Order #{self.order.id})"
