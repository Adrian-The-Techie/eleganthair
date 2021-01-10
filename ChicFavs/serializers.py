from rest_framework import serializers
from .models import EmployeeLevel, EmployeeLogins, Employees, PaymentMode, Products, Events, SaleHistory, AllocationHistory, AllocationSellingHistory, StockTakeHistory, UpdateStockHistory, Branch, ItemsSoldPerSaleHistory, Categories, ItemsAllocated, ItemsAllocatedHistory

class EmployeeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model= EmployeeLevel
        fields= "__all__"


class EmployeeLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model= EmployeeLogins
        fields= "__all__"


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Employees
        fields= "__all__"


class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model= PaymentMode
        fields= "__all__"


class EmployeeLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model= EmployeeLevel
        fields= "__all__"


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Events
        fields= "__all__"


class SaleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model= SaleHistory
        fields= ["id", "grand_total", "date_added", "emp_id", "customer_phone_number", "type_of_sale"]

class ItemsSoldPerSaleHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ItemsSoldPerSaleHistory
        fields=["id", "product_sold", "price","buying_price","quantity_sold","sub_total","sale_history_id"]


class AllocationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model= AllocationHistory
        fields= ["id","date_allocated","allocated_by"]


class AllocationSellingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model= AllocationSellingHistory
        fields= "__all__"


class StockTakingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model= StockTakeHistory
        fields= "__all__"

        
class UpdateStockSerializer(serializers.ModelSerializer):
    class Meta:
        model= UpdateStockHistory
        fields= "__all__"

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Products
        fields= "__all__"

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model= Branch
        fields= "__all__"

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields=["id", "name", "date_updated","visibility"]

class ItemsAllocatedSerializer(serializers.ModelSerializer):
    class Meta:
        model=ItemsAllocated
        fields="__all__" 

class ItemsAllocatedHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ItemsAllocatedHistory
        fields="__all__" 