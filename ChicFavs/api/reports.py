from ..models import SaleHistory, ItemsSoldPerSaleHistory, Products
from django.utils import timezone
from .api_general import genDateTimeString
from django.core.mail import EmailMessage
from django.conf import settings
import functools
import operator
import csv


def getTodaysReport():
    dateToday = timezone.now()
    itemsSoldToday = []
    finalReport = []
    sales = SaleHistory.objects.values("id", "date_added")
    # Lopp through sales to get sales sold today
    for sale in sales:
        if sale["date_added"].date() == dateToday.date():
            # Get items sold today
            sale = ItemsSoldPerSaleHistory.objects.filter(sale_history_id=sale["id"]).values(
                "product_sold", "quantity_sold", "price", "buying_price")
            for item in sale:
                productDetails = Products.objects.get(id=item["product_sold"])
                item['id'] = productDetails.id
                item["name"] = productDetails.name
                itemsSoldToday.append(item)  # Contains all items sold today
    # set of products sold today
    itemsSoldTodaySet = set(map(lambda product: product["id"], itemsSoldToday))
    for item in itemsSoldTodaySet:
        product_id = 0
        quantitySold = []
        name = ""
        buying_price = 0.00
        selling_price = 0.00
        for product in itemsSoldToday:
            if product["id"] == item:
                product_id = product["id"]
                quantitySold.append(product["quantity_sold"])
                name = product["name"]
                buying_price = product["buying_price"]
                selling_price = product["price"]
        product = {
            "id": product_id,
            "name": name,
            'buying_price': buying_price,
            'selling_price': selling_price,
            'quantity_sold': functools.reduce(operator.add, quantitySold) if len(quantitySold) > 0 else 0
        }
        product['profit'] = product['selling_price'] - product['buying_price']
        product['total_value_sold'] = product['profit'] * \
            product['quantity_sold']
        finalReport.append(product)

    # create csv file of report and send email of the report
    fileName = "Chic_favs_today's_Sale_report_as_of" + \
        genDateTimeString(timezone.now())+".csv"
    fieldNames = ["Product ID", "Product name", "Buying price",
                  "Selling price", "Quantity sold", "Profit", "Total value earned"]
    formattedReport = []
    for product in finalReport:
        product = dict(zip(fieldNames, product.values()))
        formattedReport.append(product)

    with open("ChicFavs/static/ChicFavs/documents/"+fileName, "w") as reportCsv:
        csvWriter = csv.DictWriter(reportCsv, fieldnames=fieldNames)
        csvWriter.writeheader()
        csvWriter.writerows(formattedReport)

        reportCsv.close()

    # send email
    with open("ChicFavs/static/ChicFavs/documents/"+fileName, "rb") as csvReport:
        subject = "Chic favs today's sales report as of " + \
            genDateTimeString(timezone.now())
        message = "Hello. Hope this email finds you well.\nPlease find attached today's, {}, sales report for more analysis.".format(
            dateToday.strftime("%A, %d %B %Y"))
        origin = settings.EMAIL_HOST_USER
        to = ["adrianmuthomie@gmail.com"]
        email = EmailMessage(subject, message, origin, to)
        email.attach(fileName, csvReport.read(), 'text/csv')

        email.send()

        csvReport.close()

        response = {
            "date_performed": genDateTimeString(timezone.now()),
            "details": finalReport,
            "salesValuation": functools.reduce(operator.add, map(lambda productSold: productSold["total_value_sold"], finalReport), 0),
            "message": "Report generated successfully. Please check email for a copy of it."
        }

    return response


def getMonthReport():
    dateToday = timezone.now()
    itemsSoldToday = []
    finalReport = []
    sales = SaleHistory.objects.values("id", "date_added")
    # Lopp through sales to get sales sold this month
    for sale in sales:
        if sale["date_added"].month == dateToday.month:
            # Get items sold this month
            sale = ItemsSoldPerSaleHistory.objects.filter(sale_history_id=sale["id"]).values(
                "product_sold", "quantity_sold", "price", "buying_price")
            for item in sale:
                productDetails = Products.objects.get(id=item["product_sold"])
                item['id'] = productDetails.id
                item["name"] = productDetails.name
                itemsSoldToday.append(item)  # Contains all items sold month
    # set of products sold month
    itemsSoldTodaySet = set(map(lambda product: product["id"], itemsSoldToday))
    for item in itemsSoldTodaySet:
        product_id = 0
        quantitySold = []
        name = ""
        buying_price = 0.00
        selling_price = 0.00
        for product in itemsSoldToday:
            if product["id"] == item:
                product_id = product["id"]
                quantitySold.append(product["quantity_sold"])
                name = product["name"]
                buying_price = product["buying_price"]
                selling_price = product["price"]
        product = {
            "id": product_id,
            "name": name,
            'buying_price': buying_price,
            'selling_price': selling_price,
            'quantity_sold': functools.reduce(operator.add, quantitySold) if len(quantitySold) > 0 else 0
        }
        product['profit'] = product['selling_price'] - product['buying_price']
        product['total_value_sold'] = product['profit'] * \
            product['quantity_sold']
        finalReport.append(product)

    fileName = "Chic_favs_{}_{}_sales report.csv".format(
        dateToday.strftime("%B"), dateToday.year)
    fieldNames = ["Product ID", "Product name", "Buying price",
                  "Selling price", "Quantity sold", "Profit", "Total value earned"]
    formattedReport = []
    for product in finalReport:
        product = dict(zip(fieldNames, product.values()))
        formattedReport.append(product)

    with open("ChicFavs/static/ChicFavs/documents/"+fileName, "w") as reportCsv:
        csvWriter = csv.DictWriter(reportCsv, fieldnames=fieldNames)
        csvWriter.writeheader()
        csvWriter.writerows(formattedReport)

        reportCsv.close()

    # send email
    with open("ChicFavs/static/ChicFavs/documents/"+fileName, "rb") as csvReport:
        subject = "Chic favs {} {} sales report".format(
            dateToday.strftime("%B"), dateToday.year)
        message = "Hello. Hope this email finds you well.\nPlease find attached {} {}'s sales report for more analysis.".format(
            dateToday.strftime("%B"), dateToday.year)
        origin = settings.EMAIL_HOST_USER
        to = ["adrianmuthomie@gmail.com"]
        email = EmailMessage(subject, message, origin, to)
        email.attach(fileName, csvReport.read(), 'text/csv')

        email.send()

        csvReport.close()

        response = {
            "date_performed": genDateTimeString(timezone.now()),
            "details": finalReport,
            "salesValuation": functools.reduce(operator.add, map(lambda productSold: productSold["total_value_sold"], finalReport), 0),
            "message": "Report generated successfully. Please check email for a copy of it."
        }

    return response


def getYearReport():
    dateToday = timezone.now()
    itemsSoldToday = []
    finalReport = []
    sales = SaleHistory.objects.values("id", "date_added")
    # Lopp through sales to get sales sold this year
    for sale in sales:
        if sale["date_added"].year == dateToday.year:
            # Get items sold year
            sale = ItemsSoldPerSaleHistory.objects.filter(sale_history_id=sale["id"]).values(
                "product_sold", "quantity_sold", "price", "buying_price")
            for item in sale:
                productDetails = Products.objects.get(id=item["product_sold"])
                item['id'] = productDetails.id
                item["name"] = productDetails.name
                # Contains all items sold this year
                itemsSoldToday.append(item)
    # set of products sold this year
    itemsSoldTodaySet = set(map(lambda product: product["id"], itemsSoldToday))
    for item in itemsSoldTodaySet:
        product_id = 0
        quantitySold = []
        name = ""
        buying_price = 0.00
        selling_price = 0.00
        for product in itemsSoldToday:
            if product["id"] == item:
                product_id = product["id"]
                quantitySold.append(product["quantity_sold"])
                name = product["name"]
                buying_price = product["buying_price"]
                selling_price = product["price"]
        product = {
            "id": product_id,
            "name": name,
            'buying_price': buying_price,
            'selling_price': selling_price,
            'quantity_sold': functools.reduce(operator.add, quantitySold) if len(quantitySold) > 0 else 0
        }
        product['profit'] = product['selling_price'] - product['buying_price']
        product['total_value_sold'] = product['profit'] * \
            product['quantity_sold']
        finalReport.append(product)

        fileName = "Chic_favs_{}_sales_report.csv".format(dateToday.year)
        fieldNames = ["Product ID", "Product name", "Buying price",
                      "Selling price", "Quantity sold", "Profit", "Total value earned"]
        formattedReport = []
        for product in finalReport:
            product = dict(zip(fieldNames, product.values()))
            formattedReport.append(product)

    with open("ChicFavs/static/ChicFavs/documents/"+fileName, "w") as reportCsv:
        csvWriter = csv.DictWriter(reportCsv, fieldnames=fieldNames)
        csvWriter.writeheader()
        csvWriter.writerows(formattedReport)

        reportCsv.close()

    # send email
    with open("ChicFavs/static/ChicFavs/documents/"+fileName, "rb") as csvReport:
        subject = "Chic favs {} sales report".format(dateToday.year)
        message = "Hello. Hope this email finds you well.\nPlease find attached {}'s sales report for more analysis.".format(
            dateToday.year)
        origin = settings.EMAIL_HOST_USER
        to = ["adrianmuthomie@gmail.com"]
        email = EmailMessage(subject, message, origin, to)
        email.attach(fileName, csvReport.read(), 'text/csv')

        email.send()

        csvReport.close()

        response = {
            "date_performed": genDateTimeString(timezone.now()),
            "details": finalReport,
            "salesValuation": functools.reduce(operator.add, map(lambda productSold: productSold["total_value_sold"], finalReport)),
            "message": "Report generated successfully. Please check email for a copy of it."
        }

    return response
