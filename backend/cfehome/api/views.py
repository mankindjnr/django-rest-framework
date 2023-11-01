from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view


from product.models import Product
from product.serializers import ProductSerializer


@api_view(['POST'])
def api_home(request, *args, **kwargs):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        saveddata = serializer.save() #instance
        print(serializer.data)
        data = serializer.data
        return Response(data)



"""
@api_view(['GET'])
def api_home(request, *args, **kwargs):
    #Django rest framework view
    instance = Product.objects.all().order_by("?").first()
    data = {}

    if instance:
        #data = model_to_dict(model_data)
        data = ProductSerializer(instance).data
    return Response(data)


def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    data = {}

    if model_data:
        data = model_to_dict(model_data)
    return JsonResponse(data)
"""