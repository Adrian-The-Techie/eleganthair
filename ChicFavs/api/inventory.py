import datetime
from ..models import ItemsAllocated, Employees, AllocationHistory, ItemsAllocatedHistory, Products
class InventoryMngt:

    def __init__(self, data):
        self.data=data

    def allocateStock(self):
        response={}
        emp_allocated_to=Employees.objects.get(id=self.data["allocated_to"])
        allocated_by=Employees.objects.get(id=self.data["allocated_by"])
        allocationHistoryInstance=AllocationHistory(emp_allocated_to=emp_allocated_to, allocated_by=allocated_by)
        allocationHistoryInstance.save()

        for item in self.data["items"]:
            productInstance=Products.objects.get(id=item["product_allocated"])
            try:
                itemAllocated= ItemsAllocated.objects.get(product_allocated_to=allocationHistoryInstance.emp_allocated_to,product_allocated=item["product_allocated"])
                if itemAllocated != None:
                    itemAllocated.quantity_allocated +=item["quantity_allocated"]
                    itemAllocated.date_updated=datetime.datetime.now()
                    itemAllocated.save()
            except ItemsAllocated.DoesNotExist:
                itemAllocatedInstance=ItemsAllocated(product_allocated=productInstance,quantity_allocated=item["quantity_allocated"],product_allocated_to=allocationHistoryInstance.emp_allocated_to)
                itemAllocatedInstance.save()

            # deduct from product's quantity in stock
            productInstance.quantity_in_stock -= item["quantity_allocated"]
            productInstance.save()
            
            # save allocation history
            itemsAllocatedHistoryInstance=ItemsAllocatedHistory(allocation_history=allocationHistoryInstance, product=productInstance,quantity_allocated=item["quantity_allocated"])
            itemsAllocatedHistoryInstance.save()

        response={
            "status":1,
            "data":"Items allocated successfully"
        }

        return response