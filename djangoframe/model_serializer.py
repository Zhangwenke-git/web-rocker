from rest_framework.serializers import ModelSerializer
from .models import *

from rest_framework.filters import SearchFilter


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
        filter_backends = (SearchFilter,)