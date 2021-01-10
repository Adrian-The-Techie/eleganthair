import datetime
import functools
import operator
import csv
from ..serializers import *
from ..auth import Auth
from .sales import SalesMngt
from .api_general import sendSms, genDateTimeString
from .inventory import InventoryMngt
from .reports import getTodaysReport, getMonthReport, getYearReport
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.core.files import File

class API:

    def __init__(self, data):
        self.data = data
    
    #  main api function
    def apis(self):
        responseData = {}
        response = ""

        if self.data["apiid"] == "saveEmployeeLevels":
            serializer = EmployeeLevelSerializer(data = self.data["data"])

            if serializer.is_valid():
                serializer.save()
                responseData = {
                    "status":1,
                    "data": serializer.data
                }
            else:
                responseData = {
                    "status":0,
                    "data": "Error occured. Was not able to save. Please try again later"
                }
        if self.data["apiid"] == "getEmployeeLevels":
            employeeLevels = EmployeeLevel.objects.all()
            serializer = EmployeeLevelSerializer(employeeLevels, many=True)

            responseData = {
                "status":1,
                "data": serializer.data
            }
        if self.data["apiid"] =="updateEmployeeLevel":
            data = {
                "name": self.data["data"]["updatedLevel"],
                "level":self.data["data"]["level"],
                "date_updated": datetime.datetime.now()
            }
            employeeLevels = EmployeeLevel.objects.get(id=self.data["data"]["id"])
            serializer = EmployeeLevelSerializer(instance=employeeLevels, data=data)

            if serializer.is_valid():
                serializer.save()
                responseData = {
                    "status":1,
                    "data": serializer.data["name"]
                }
        if self.data["apiid"]=="deleteEmployeeLevel":
            employeeLevel = EmployeeLevel.objects.get(id= self.data["data"])
            response = employeeLevel.delete()

            responseData = {
                "status": 1,
                "data": response
            }
        
        if self.data["apiid"] == "loadEmployeeLevels":
            response = EmployeeLevel.objects.only('name')
            data = EmployeeLevelSerializer(response, many= True)

            responseData= {
                "status":1,
                "data": data.data
            }

        if self.data["apiid"] == "saveEmployee":
            responseData = {
                "status":1,
                "data":Auth(data=self.data["data"]).newUser()
            }
        if self.data["apiid"] == "login":
            responseData=Auth(data=self.data["data"]).login()

        if self.data["apiid"] == "checkLoginStatus":
            response=Auth(data=self.data["data"]).checkLoginStatus()

        if self.data["apiid"] == "getAllEmployees":
            employees = Employees.objects.all()
            serializer= EmployeesSerializer(employees, many=True)
            for i in serializer.data:
                emp_level_details = EmployeeLevel.objects.get(pk=i["emp_level"])
                emp_branch_details = Branch.objects.get(pk=i["branch"])

                serializedLevelDetails= EmployeeLevelSerializer(emp_level_details, many=False)
                serializedBranchDetails= BranchSerializer(emp_branch_details, many=False)

                i["emp_level"] = serializedLevelDetails.data
                i["branch"] = serializedBranchDetails.data

            responseData = {
                "status":1,
                "data": serializer.data
            }
        
        if self.data["apiid"] == "updateEmployeeDetails" :
            self.data["data"]["date_updated"] = datetime.datetime.now()
            employeeInstance= Employees.objects.get(id=self.data["data"]["id"])
            serializer = EmployeesSerializer(instance = employeeInstance, data=self.data["data"] )

            if serializer.is_valid():
                serializer.save()

                responseData ={
                    "status":1,
                    "data":serializer.data["username"]
                }
            else:
                responseData ={
                    "status":0,
                    "data":serializer.errors
                }
        if self.data["apiid"] == "deleteEmployee":
            employeeInstance= Employees.objects.get(id= self.data["data"]["id"])
            employeeInstance.visibility=0
            response = employeeInstance.save()
            responseData = {
                "status": 1,
                "data": employeeInstance.username
            }
        
        if self.data["apiid"] == "saveNewProduct":
            data={
                "name":self.data["name"],
                "buying_price":self.data["buying_price"],
                "selling_price":self.data["selling_price"],
                "quantity_in_stock":self.data["quantity_in_stock"],
                "category":self.data["category"]
            }

            if "image" not in self.data:
                pass
            else:
                data["image"]=self.data["image"]

            serializer = ProductsSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                responseData={
                    "status":1,
                    "data":serializer.data["name"]
                }
            else:
                responseData= {
                    "status":0,
                    "data":serializer.errors
                }
            # print (self.data)
            
        if self.data["apiid"] == "getAllProducts":
            products = Products.objects.filter(visibility=1)
            serializer = ProductsSerializer(products, many=True)

            responseData= {
                "status":1,
                "data": serializer.data
            }
        if self.data["apiid"]== "searchProducts":
            matchedProducts= Products.objects.filter(name_icontains= self.data["data"]["searchString"])
            serializer= ProductsSerializer(matchedProducts, many= True)

            responseData= {
                "status":1,
                "data":serializer.data
            }


        if self.data["apiid"] == "updateProductDetails":
            productInstance = Products.objects.get(pk= self.data["id"])
            data={
                "name":self.data["name"],
                "buying_price":self.data["buying_price"],
                "selling_price":self.data["selling_price"],
                "quantity_in_stock":self.data["quantity_in_stock"],
                "date_updated": datetime.datetime.now()
            }
            if "image" not in self.data:
                pass
            else:
                data["image"]=self.data["image"]

            serializer = ProductsSerializer(instance= productInstance, data=data)

            if serializer.is_valid():
                serializer.save()
                responseData= {
                    "status":1,
                    "data":serializer.data["name"]
                }
            else:
                responseData= {
                    "status":0,
                    "data": serializer.errors
                }
            
        if self.data["apiid"] == "deleteProduct":
            productDetails = Products.objects.get(pk=self.data["data"]["id"])
            productDetails.visibility=0
            response= productDetails.save()

            responseData= {
                "status":1,
                "data": "Product deleted successfuly"
            }

        if self.data["apiid"] == "saveNewBranch":
            serializer = BranchSerializer(data = self.data["data"])

            if serializer.is_valid():
                serializer.save()
                responseData = {
                    "status":1,
                    "data": serializer.data
                }
            else:
                responseData = {
                    "status":0,
                    "data": "Error occured. Was not able to save. Please try again later"
                }
        if self.data["apiid"] == "getBranches":
            branches = Branch.objects.all()
            serializer = BranchSerializer(branches, many=True)

            responseData = {
                "status":1,
                "data": serializer.data
            }
        if self.data["apiid"] =="updateBranch":
            data = {
                "name": self.data["data"]["updatedBranch"],
                "date_updated": datetime.datetime.now()
            }
            branch = Branch.objects.get(id=self.data["data"]["id"])
            serializer = BranchSerializer(instance=branch, data=data)

            if serializer.is_valid():
                serializer.save()
                responseData = {
                    "status":1,
                    "data": serializer.data["name"]
                }
        if self.data["apiid"]=="deleteBranch":
            branch = Branch.objects.get(id= self.data["data"])
            response = branch.delete()

            responseData = {
                "status": 1,
                "data": response
            }
        if self.data["apiid"] == "makeASale":
            response=SalesMngt(self.data["data"]).makeASale()
            if response["SMSMessageData"]["Recipients"][0]["status"]=="Success":
                responseData={
                    "status":1,
                    "data":"Sale made successfully"
                }
            else:
                responseData={
                    "status":0,
                    "data":"Error sending message. Please try again"
                }
        if self.data["apiid"] == "getSaleHistory":
            sales= SaleHistory.objects.values("id", "customer_phone_number","date_added")
            # serializer=SaleHistorySerializer(sales)
            for sale in sales:
                sale["date_added"]=genDateTimeString(sale["date_added"])
            responseData={
                "status":1,
                "data":sales
            }
        if self.data["apiid"] == "getSpecificSaleHistoryDetails":
            specificSaleHistory= SaleHistory.objects.get(id=self.data["data"]["id"])
            specificSaleHistory.date_added=genDateTimeString(dateObj=specificSaleHistory.date_added)
            serializedSaleHistory=SaleHistorySerializer(specificSaleHistory, many=False)
            values=serializedSaleHistory.data
            values["type_of_sale"]="Normal sale" if values["type_of_sale"] == 1 else "Allocation sale"
            employee=Employees.objects.get(id=values["emp_id"])
            values["emp_id"]=employee.username
            items= ItemsSoldPerSaleHistory.objects.filter(sale_history_id=values["id"]).values("id", "product_sold_id", "price","quantity_sold","sub_total")
            values["items_sold"]=items
            for specificItem in values["items_sold"]:
                name=Products.objects.get(id=specificItem["product_sold_id"])
                specificItem["product_sold_id"]=name.name
            
            responseData={
                "status":1,
                "data":values
            }
        if self.data["apiid"] == "resendReceipt":
            itemsString=""
            for item in self.data["data"]["items"]:
                itemsString +=item["product_sold_id"]+", "+str(item["quantity_sold"])+" piece(s), "+str(item["price"])+" per piece, sub-total is "+str(item["sub_total"])+"\n"

            message="Here is your receipt;\nReceipt ID: "+str(self.data["data"]["receiptId"])+"\n"+itemsString+"\n Sold by: "+self.data["data"]["sold_by"]+"\n GRAND TOTAL: "+self.data["data"]["amount_sold"]+"\n Sold on "+self.data["data"]["sold_on"]
            response=sendSms(self.data["data"]["recipient"], message)

            if response["SMSMessageData"]["Recipients"][0]["status"]=="Success":
                responseData={
                    "status":1,
                    "data":"Receipt resent successfully"
                }
            else:
                responseData={
                    "status":0,
                    "data":"Error sending message. Please try again"
                }
        if self.data["apiid"] == "saveNewCategory":
            serializer = CategoriesSerializer(data = self.data["data"])

            if serializer.is_valid():
                serializer.save()
                responseData = {
                    "status":1,
                    "data": serializer.data
                }
            else:
                responseData = {
                    "status":0,
                    "data": "Error occured. Was not able to save. Please try again later"
                }
        if self.data["apiid"] == "getCategories":
            categories = Categories.objects.values("id", "name")

            responseData = {
                "status":1,
                "data": categories
            }
        if self.data["apiid"] =="updateCategory":
            data = {
                "name": self.data["data"]["updatedCategory"],
                "date_updated": datetime.datetime.now()
            }
            category = Categories.objects.get(id=self.data["data"]["id"])
            serializer = CategoriesSerializer(instance=category, data=data)

            if serializer.is_valid():
                serializer.save()
                responseData = {
                    "status":1,
                    "data": serializer.data["name"]
                }
        if self.data["apiid"]=="deleteCategory":
            category = Categories.objects.get(id= self.data["data"])
            response = category.delete()

            responseData = {
                "status": 1,
                "data": "Category deleted successfully"
            }
        
        if self.data["apiid"] == "getUserAndProducts":
            salesPeople=Employees.objects.filter(emp_level=2).values("id","username")
            products=Products.objects.values("id", "name","quantity_in_stock","selling_price")

            responseData={
                "status":1,
                "data":{
                    "salesPeople":salesPeople,
                    "products":products
                }
            }
        if self.data["apiid"] == "allocateStock":
            responseData=InventoryMngt(self.data["data"]).allocateStock()

        if self.data["apiid"] == "getAllSalespeople":
            salesPeople=Employees.objects.filter(emp_level=2).values("id", "username")
            responseData={
                "status":1,
                "data":salesPeople
            }
        if self.data["apiid"] == "getSpecificAllocationDetails":
            user_id=self.data["data"]["id"]
            availableItems=ItemsAllocated.objects.filter(product_allocated_to=user_id).values("product_allocated","quantity_allocated")
            allocationHistory=AllocationHistory.objects.filter(emp_allocated_to=user_id).values("id","date_allocated")

            for item in availableItems:
                itemInstance=Products.objects.get(id=item["product_allocated"])
                item["product_allocated"]=itemInstance.name

            for specificHistory in allocationHistory:
                specificHistory["date_allocated"]=genDateTimeString(specificHistory["date_allocated"])
        
            responseData={
                "status":1,
                "data":{
                    "availableItems":availableItems,
                    "allocationHistory":allocationHistory
                }
            }

        if self.data["apiid"] == "getSpecificAllocationHistoryDetails":
            specificAllocationHistory= AllocationHistory.objects.get(id=self.data["data"]["id"])
            specificAllocationHistory.date_allocated=genDateTimeString(dateObj=specificAllocationHistory.date_allocated)
            serializedAllocationHistory=AllocationHistorySerializer(specificAllocationHistory, many=False)
            values=serializedAllocationHistory.data
            allocated_by=Employees.objects.get(id=values["allocated_by"])
            values["allocated_by"]=allocated_by.username
            items= ItemsAllocatedHistory.objects.filter(allocation_history=values["id"]).values("id", "product","quantity_allocated")
            values["items_sold"]=items
            for specificItem in values["items_sold"]:
                product=Products.objects.get(id=specificItem["product"])
                specificItem["product"]=product.name
                specificItem["selling_price"]=product.selling_price
                specificItem["sub_total_value"]=specificItem["selling_price"] * specificItem["quantity_allocated"]
            # get grand total
            subTotals=list(map(lambda item:item["sub_total_value"], values["items_sold"]))
            values["grand_total_value"]=functools.reduce(operator.add,subTotals) if len(subTotals)>0 else 0

            responseData={
                "status":1,
                "data":values
            }

        if self.data["apiid"] == "getSellingProducts":
            products={}
            if self.data["data"]["type_of_sale"] == 1:
                products=Products.objects.values("id","name","selling_price","quantity_in_stock","buying_price")

            else:
                products=ItemsAllocated.objects.filter(product_allocated_to=self.data["data"]["user_id"]).values("id","product_allocated","quantity_allocated")
                for product in products:
                    productInstance=Products.objects.get(id=product["product_allocated"])
                    product["name"]=productInstance.name
                    product["selling_price"]=productInstance.selling_price
                    product["buying_price"]=productInstance.buying_price

            responseData={
                "status":1,
                "data":products
            }

        if self.data["apiid"] == "performStockTake":
            productsQuantityInStock= Products.objects.values("id", "name", "quantity_in_stock", "selling_price")
            subTotalValueList=[]

            for product in productsQuantityInStock:
                itemAllocatedQuantityInStock=ItemsAllocated.objects.filter(product_allocated=product["id"]).values("quantity_allocated")
                product["item_allocated_quantity_in_stock"]=itemAllocatedQuantityInStock
                quantity_in_stock= map(lambda product:product["quantity_allocated"], product["item_allocated_quantity_in_stock"])
                product["item_allocated_quantity_in_stock"]=quantity_in_stock
                product["item_allocated_quantity_in_stock"]= functools.reduce(operator.add, product["item_allocated_quantity_in_stock"],0)
                product["total_quantity_in_stock"]=product["quantity_in_stock"] + product["item_allocated_quantity_in_stock"]
                product["sub_total_value"]=product["total_quantity_in_stock"] * product["selling_price"]

                subTotalValueList.append(product["sub_total_value"])
            # CREATE CSV FILE, SAVE AND EMAIL
            # create
            currentDateTime=genDateTimeString(datetime.datetime.now())
            fieldNames=["Product ID", "Product Name", "Quantity in stock for normal sale", "Selling price","Quantity in stock for allocation sale", "Total quantity in stock", "Total valuation of product"]
            formattedData=[]

            #change product key to be readable in csv
            for item in productsQuantityInStock:
                item=dict(zip(fieldNames, list(item.values())))
                formattedData.append(item)
                
            fileName="Stock_report_as_of_"+currentDateTime+".csv"
            
            with open("pos/static/pos/documents/"+fileName, "a+") as csvFile:
                finalFile=File(csvFile)
                csvFileObject=csv.DictWriter(csvFile, fieldnames=fieldNames)
                csvFileObject.writeheader()
                csvFileObject.writerows(formattedData)
            # save
                stockTakeHistoryInstance=StockTakeHistory(csv_file=finalFile.name)
                stockTakeHistoryInstance.save()

                finalFile.close()
            # email
            # try:
            with open("pos/static/pos/documents/"+fileName, "rb") as report:
                subject="STOCK REPORT"
                message="Hello. Please find attached the stock report as of "+currentDateTime
                origin=settings.EMAIL_HOST_USER
                to=["adrianmuthomie@gmail.com"]
                email=EmailMessage(subject, message, origin, to)
                email.attach(fileName, report.read(), "text/csv")
                email.send()

                report.close()
            # except Exception as e:
            #     responseData={
            #         "status":0,
            #         "data":"Error: {}".format(e)
            #     }

            responseData={
                "status":1,
                "data":{
                    "date_performed":genDateTimeString(timezone.now()),
                    "details":productsQuantityInStock,
                    "stockValuation":functools.reduce(operator.add, subTotalValueList),
                    "message":"Report generated successfully. Check email to view report"
                }
            }
        
        if self.data["apiid"] == "getStockTakeHistories":
            stockTakeHistories= StockTakeHistory.objects.values("id", "date_added")
            for history in stockTakeHistories:
                history["date_added"]=genDateTimeString(history["date_added"])

            responseData={
                "status":1,
                "data":stockTakeHistories
            }

        if self.data["apiid"] == "getSpecificStockTakeHistory":
            stockTakeHistoryInstance=StockTakeHistory.objects.get(id=self.data["data"]["id"])
            csvFile=stockTakeHistoryInstance.csv_file.name
            dictKeys=["id","name","quantity_in_stock","selling_price","item_allocated_quantity_in_stock","total_quantity_in_stock","sub_total_value"]
            products=[]
            formattedProducts=[]
            subTotalValueList=[]

            # read retrieved csv to a dictionary and append to list
            with open(csvFile, "r") as report:
                csvReader=csv.DictReader(report)
                for line in csvReader:
                    line["Product ID"]=int(line["Product ID"])
                    line["Quantity in stock for normal sale"]=int(line["Quantity in stock for normal sale"])
                    line["Selling price"]=float(line["Selling price"])
                    line["Quantity in stock for allocation sale"]=float(line["Quantity in stock for allocation sale"])
                    line["Total quantity in stock"]=float(line["Total quantity in stock"])
                    line["Total valuation of product"]=float(line["Total valuation of product"])

                    products.append(line)
                report.close()

            # format data to be compatible in frontend
            for product in products:
                product=dict(zip(dictKeys, product.values()))
                formattedProducts.append(product)
                subTotalValueList.append(float(product["sub_total_value"]))

            responseData={
                "status":1,
                "data":{
                    "details":formattedProducts,
                    "date_performed":genDateTimeString(stockTakeHistoryInstance.date_added),
                    "stockValuation":functools.reduce(operator.add,subTotalValueList)
                }
            }

        if self.data["apiid"] == "getTodaysReport":
            # get today's sales
            response=getTodaysReport()

            responseData={
                "status":1,
                "data":response
            }
        
        if self.data["apiid"] == "getMonthReport":
            # get this month's sales
            response=getMonthReport()

            responseData={
                "status":1,
                "data":response
            }

        if self.data["apiid"] == "getYearReport":
            # get this year's sales
            response=getYearReport()

            responseData={
                "status":1,
                "data":response
            }

        return responseData
        