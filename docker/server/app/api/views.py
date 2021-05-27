from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from api import utils


@api_view(['POST'])
def upload_data(request):
    if request.method == 'POST':
        try:
            data = request.data
            utils.save_data(data)
            return HttpResponse(status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error in upload: ", e)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)