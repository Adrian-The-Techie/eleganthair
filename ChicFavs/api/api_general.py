import requests
from .config import API_KEY, SMS_API, USERNAME
import pytz


def sendSms(recipient, message):
    requestData = {
        "to": [recipient],
        "message": message,
        "username": USERNAME
    }
    headers = {
        "apikey": "iIitfewFbqrtkLTRNNRMCns04jHqAkXxO02OwXY3Y61JBiDcHx",
        "Content-Type": "application/x-www-form-urlencoded",
        "cache-control": "no-cache"
    }
    response = requests.post("https://sms.movesms.co.ke/api/compose", params={
        "username": "RODWELL",
        "api_key": "iIitfewFbqrtkLTRNNRMCns04jHqAkXxO02OwXY3Y61JBiDcHx",
        "sender": "SMARTLINK",
        "to": recipient,
        "message": message,
        # "msgtype": 5,
        # "dlr": 1
    }, headers=headers)

    return response.content


def genDateTimeString(dateObj):
    naiTimeZone = pytz.timezone("Africa/Nairobi")
    naiTime = dateObj.astimezone(naiTimeZone)
    dateString = naiTime.strftime("%a, %d %b %Y at %I:%M:%S%p")

    return dateString
