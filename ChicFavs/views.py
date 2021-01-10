from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .api.api import API

# Create your views here.


@api_view(["POST"])
def index(request):
    response = API(data=request.data).apis()

    return Response(response)
