from django.shortcuts import render
from django.http import httpResponse

def home (request):
    return httpResponse("Yes sirr django server ecommerce")

# Create your views here.
