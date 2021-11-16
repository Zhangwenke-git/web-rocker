from django.urls import path,re_path
from djangoframe import views
app_name='restful'

urlpatterns = [
    path('employee/',views.employeeListView,name='employee_list_view'),
    re_path(r'^employee/(\d+)/$',views.employeeDetailView,name='employee_detail_view'),
]