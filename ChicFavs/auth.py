import os
import hashlib
import jwt
import datetime
from .serializers import EmployeesSerializer
from .models import Employees, EmployeeLevel,Branch, EmployeeLogins
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class Auth:

    def __init__(self, data):
        self.data = data

    def hashPassword(self, data):
        key = make_password(data)

        return key

    def newUser(self):
        employeeLevel=EmployeeLevel.objects.get(id=self.data["emp_level"])
        branch=Branch.objects.get(id=self.data["branch"])
        employee =Employees.objects.create_user(
            username=self.data["name"],
            phone_number=self.data["phone"],
            place_of_residence=self.data["residence"],
            email=self.data["email"],
            emp_level=employeeLevel,
            branch=branch,
            password=self.data["password"]
        )
        return employee.username

    def login(self):
        response={}
        try:
            user= authenticate(username=self.data["username"], password=self.data["password"])
            if user != None and user.visibility != 0:
                userLoginInstance=EmployeeLogins(is_logged_in=True, device_info=self.data["username"], employee_id=user.id)
                userLoginInstance.save()
                response={
                    "status":1,
                    "data":{
                        "message":"Login successful",
                        "user_id":user.id,
                        "level":user.emp_level.level,
                        "userLoginInstance":userLoginInstance.id
                    }
                    
                }
            else:
                response={
                    "status":0,
                    "data":"Invalid credentials. Please try again"
                }
        except Employees.DoesNotExist:
            response={
                    "status":0,
                    "data":"User does not exist. Please contact admin for assistance"
                }

        return response

    def checkLoginStatus(self):
        try:
            employeeLoginInstance=EmployeeLogins.objects.get(id=self.data['id'])
            if employeeLoginInstance.is_logged_in == True:
                response={
                    "status":1,
                    "data":"User is logged in"
                }
            else:
                response={
                    "status":0,
                    "data":"Please Login"
                }
        except:
            response={
                "status":0,
                "data":"Error checking your login status"
            }

