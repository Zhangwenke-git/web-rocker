from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import *
from .model_serializer import *
from .exceptions import FailureResponse,SuccessResponse

@api_view(["GET","POST"])
def employeeListView(request):
    if request.method == "GET":
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset,many=True)
        raise SuccessResponse(result=serializer.data)
    elif request.method=="POST":
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            raise FailureResponse("10001",serializer.errors)

@api_view(["GET","PUT","DELETE"])
def employeeDetailView(request,id):
    try:
        queryset = Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        raise FailureResponse(code="10005",message="该人员信息不存在，请确认查询条件")
    else:
        if request.method=="GET":
            serializer = EmployeeSerializer(queryset,many=False)
            raise SuccessResponse(result=serializer.data)
        elif request.method == "PUT":
            serializer = EmployeeSerializer(queryset,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            queryset.delete()
            return Response(status=status.HTTP_200_OK)
