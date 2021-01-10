import requests
from .config import API_KEY, SMS_API, USERNAME
import pytz

def sendSms(recipient,message):
    requestData={
        "to":[recipient],
        "message":message,
        "username":USERNAME
    }
    headers={
        "apiKey":API_KEY,
        "Content-Type":"application/x-www-form-urlencoded",
        "Accept":"application/json"
    }
    response=requests.post(url=SMS_API, data=requestData, headers=headers)

    return response.json()

def genDateTimeString(dateObj):
    naiTimeZone=pytz.timezone("Africa/Nairobi")
    naiTime=dateObj.astimezone(naiTimeZone)
    dateString=naiTime.strftime("%a, %d %b %Y at %I:%M:%S%p")

    return dateString