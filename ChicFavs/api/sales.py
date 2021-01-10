from ..serializers import *
import requests
from .api_general import sendSms, genDateTimeString
import pytz

class SalesMngt:
    
    def __init__(self, data):
        self.data=data


    def makeASale(self):
        phoneNumber=self.data["phoneNumber"]
        itemsString=""
        employee=Employees.objects.get(id=self.data["sold_by"])
        # Save sale history 
        saleHistoryInstance= SaleHistory(grand_total=self.data["grand_total"], customer_phone_number=phoneNumber,emp_id=employee, type_of_sale=self.data["type_of_sale"])
        saleHistoryInstance.save()
        for item in self.data["items"]:
            # get product
            item.pop("name")
            item["sale_history_id"]=saleHistoryInstance.id

            serializer= ItemsSoldPerSaleHistorySerializer(data=item)

            if serializer.is_valid():
                serializer.save()
                productInstance= Products.objects.get(id=serializer.data["product_sold"])
                # deduct stock after sale
                if saleHistoryInstance.type_of_sale == 1:
                    productInstance.quantity_in_stock -= serializer.data["quantity_sold"]
                    productInstance.save()
                else:
                    itemAllocatedInstance=ItemsAllocated.objects.get(product_allocated=productInstance,product_allocated_to=self.data["sold_by"])
                    itemAllocatedInstance.quantity_allocated -= item["quantity_sold"]
                    itemAllocatedInstance.save()

                itemsString +=productInstance.name+", "+str(serializer.data["quantity_sold"])+" piece(s), "+str(serializer.data["price"])+" per piece, sub-total is "+str(serializer.data["sub_total"])+"\n"
                
        dateString=genDateTimeString(dateObj=saleHistoryInstance.date_added)
        message="Here is your receipt;\nReceipt ID: "+str(saleHistoryInstance.id)+"\n"+itemsString+"\n Sold by: "+employee.username+"\n GRAND TOTAL: "+str(saleHistoryInstance.grand_total)+"\n Sold on "+dateString
        response=sendSms(phoneNumber, message)

        return response
        