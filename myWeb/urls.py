from django.contrib import admin
from django.conf.urls import handler404, handler500
from django.urls import path,re_path

from api import views as api_view
from myWeb import views as myWeb_view
from core import views as core_view
from public import views as public_view

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', myWeb_view.test),
    path('login/', myWeb_view.auth_login,name='login'),
    path('logout/', myWeb_view.auth_logout,name='logout'),
    path('lock/', myWeb_view.lock_account,name='lock'),
    path('register/', myWeb_view.register,name='register'),
    path('home/', myWeb_view.home,name="home"),
    path('profile/', myWeb_view.profile,name="profile"),
    path('guid/', myWeb_view.guid,name="guid"),
    path('about/', myWeb_view.about,name="about"),

    path('api/overview/', api_view.api_overview,name='api_overview'),
    path('api/scenarios/add/', api_view.api_scenarios,name='api_scenarios'),
    re_path(r'^(\w+)/(\w+)/(\d+)/execute/$', core_view.api_execute,name="api_execute"),
    path('api/scenarios/display_param/', api_view.display_param,name='display_param'),
    path('api/report/', api_view.api_report,name='api_report'),
    path('api/analytics/', api_view.api_analytics,name='api_analytics'),

    path('public/overview/', public_view.public_overview, name='public_overview'),
    path('public/config/', public_view.public_config, name='public_config'),
    path('public/task/', public_view.public_task, name='public_task'),
    path('public/test/', public_view.public_test, name='public_test'),
    path('public/functions/search/', public_view.public_func_search, name='public_func_search'),
    re_path(r'^public/functions/(\w+)/$', public_view.public_func_strict_search, name='public_func_strict_search'),
    path('todo/list/', public_view.todo, name='todo_list'),
    path('public/retrieval/search/', public_view.retrieval_search, name='retrieval_search'),
    path('public/request/', public_view.public_request, name='public_request'),
    path('public/dbconnect/1/', public_view.public_dbconnect_tab1, name='public_dbconnect_tab1'),
    path('public/dbconnect/2/', public_view.public_dbconnect_tab2, name='public_dbconnect_tab2'),
    path('public/dbconnect/3/', public_view.public_dbconnect_tab3, name='public_dbconnect_tab3'),
    path('public/log/1/', public_view.public_log_tab1, name='public_log_tab1'),
    path('public/compare/1/', public_view.public_compare_tab1, name='public_compare_tab1'),
    path('public/json/format/', public_view.public_json_format, name='public_json_format'),
    path('table/log/check/', public_view.display_process_log, name='display_process_log'),

    re_path(r'^(\w+)/(\w+)/$', core_view.table_data_list,name="table_data_list"),
    re_path(r'^(\w+)/(\w+)/(\d+)/update/$', core_view.table_data_update,name="table_data_update"),
    re_path(r'^(\w+)/(\w+)/add/$', core_view.table_data_add,name="table_data_add"),
    re_path(r'^(\w+)/(\w+)/(\d+)/delete/$', core_view.table_data_delete,name="table_data_delete"),

    re_path(r'^(\w+)/(\w+)/(\d+)/password/$', core_view.password_reset,name="password_reset"),
    path('password/quick/reset/', core_view.quick_password_reset,name="quick_password_reset"),
    re_path(r'^(\w+)/(\w+)/password/$', core_view.password_add,name="password_add"),
    re_path(r'^(\w+)/(\w+)/(\d+)/check/$', api_view.check_template,name="check_template"),

]

handler404 = myWeb_view.page_not_found
handler500 = myWeb_view.internal_error
