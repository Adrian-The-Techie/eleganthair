from django.db import models
from django.contrib.auth.models import AbstractUser
# from .model_defaults import *

# Create your models here.


class EmployeeLevel(models.Model):
    name = models.CharField(max_length=70)
    level = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    visibility = models.BooleanField(default=True)


class Events(models.Model):
    name = models.CharField(max_length=70)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    visibility = models.BooleanField(default=True)


class Branch(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    visibility = models.BooleanField(default=1)


class PaymentMode(models.Model):
    type = models.CharField(max_length=20)
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    shortcode = models.IntegerField(null=True)
    username = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(null=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True)


class Categories(models.Model):
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    visibility = models.BooleanField(default=True)


class Products(models.Model):
    image = models.ImageField(
        upload_to="images/", default="images/thumbnail.png")
    name = models.CharField(max_length=255)
    selling_price = models.FloatField()
    buying_price = models.FloatField()
    quantity_in_stock = models.IntegerField()
    date_added = models.DateTimeField(null=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    visibility = models.BooleanField(default=True)
    category = models.ForeignKey(
        Categories, null=True, on_delete=models.SET_NULL, default=10)


class Employees(AbstractUser):
    # def get_or_create_branch():
    #     return Branch.objects.get_or_create(name="Head office")[0].id

    # def get_or_create_level():
    #     return EmployeeLevel.objects.get_or_create(name="Uncategorized")[0].id
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=70, null=True)
    place_of_residence = models.CharField(max_length=70)
    emp_level = models.ForeignKey(
        EmployeeLevel, on_delete=models.SET_NULL, null=True, default=1)
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    visibility = models.BooleanField(default=1)


class EmployeeLogins(models.Model):
    employee = models.ForeignKey(
        Employees, on_delete=models.SET_NULL, null=True)
    is_logged_in = models.BooleanField()
    device_info = models.CharField(max_length=255, null=True)
    time_logged_in = models.DateTimeField(null=True, auto_now_add=True)
    time_logged_out = models.DateTimeField(null=True)


class SaleHistory(models.Model):
    grand_total = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    emp_id = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True)
    payment_mode = models.ForeignKey(
        PaymentMode, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=150, null=True)
    type_of_sale = models.IntegerField()
    customer_phone_number = models.CharField(
        max_length=255, default="0700000000")


class ItemsSoldPerSaleHistory(models.Model):
    sale_history_id = models.ForeignKey(
        SaleHistory, on_delete=models.SET_NULL, null=True)
    product_sold = models.ForeignKey(
        Products, on_delete=models.SET_NULL, null=True)
    quantity_sold = models.FloatField()
    buying_price = models.FloatField()
    price = models.FloatField()
    sub_total = models.FloatField()


class AllocationSellingHistory(models.Model):
    product_sold = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    total_value_sold = models.IntegerField()
    date_sold = models.DateTimeField(auto_now_add=True)
    payment_mode = models.ForeignKey(
        PaymentMode, on_delete=models.SET_NULL, default=1, null=True)
    emp_id = models.ForeignKey(
        Employees, on_delete=models.SET_NULL, default=1, null=True)
    transaction_id = models.CharField(max_length=150)
    event_sold = models.ForeignKey(
        Events, on_delete=models.SET_NULL, null=True)


class StockTakeHistory(models.Model):
    csv_file = models.FileField(upload_to="documents/")
    date_added = models.DateTimeField(auto_now_add=True)


class UpdateStockHistory(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantityupdated = models.IntegerField()
    total_value_updated = models.IntegerField()
    date_updated = models.DateTimeField(auto_now_add=True)
    emp_id = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True)


class AllocationHistory(models.Model):
    emp_allocated_to = models.ForeignKey(
        Employees, null=True, on_delete=models.SET_NULL, related_name="emp_allocated_to")
    date_allocated = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    allocated_by = models.ForeignKey(
        Employees, null=True, on_delete=models.SET_NULL, related_name="allocated_by")
    visibility = models.BooleanField(default=True)


class ItemsAllocatedHistory(models.Model):
    allocation_history = models.ForeignKey(
        AllocationHistory, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    quantity_allocated = models.FloatField()
    # event_id = models.ForeignKey(Events, on_delete=models.SET_NULL, null=True)


class ItemsAllocated(models.Model):
    product_allocated = models.ForeignKey(
        Products, null=True, on_delete=models.SET_NULL)
    quantity_allocated = models.FloatField()
    product_allocated_to = models.ForeignKey(
        Employees, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    visibility = models.BooleanField(default=True)


# create defaults
