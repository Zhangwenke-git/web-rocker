import json
import ast
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from urllib.parse import parse_qs, urlparse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from core.app_load import app_loader
from utils.pubulic.logger import Logger
from core.base_admin import site
from core.permissions import check_permission
from utils.pubulic.DBUtil import DBconnect
from public.models import Dbinfo, LogServerinfo, FirstLayerMenu
from utils.pubulic.paramikoUtil import MyParamiko
from django.utils.safestring import mark_safe
from utils.compare.CompareTemplate2 import GenerateCompareReport
from django.forms.models import model_to_dict
from core.exceptions import DefaultError, DefinedSuccess, DefinedtError

app_loader("public")
app_loader("api")
app_loader("web")
logger = Logger("public view")
table = site.registered_sites.get("public")
api_table = site.registered_sites.get("api")
web_table = site.registered_sites.get("web")
app = "public"
api_app = "api"
web_app = "web"


@login_required
def public_overview(request):
    func_name = public_overview.__name__
    menus_obj = FirstLayerMenu.objects.filter(url_name=func_name).first()
    firstmenus = model_to_dict(menus_obj).get("id")
    return render(request, 'public/overview.html', {"table": table, "app": app, "firstmenus": firstmenus})


@login_required
def public_config(request):
    func_name = public_config.__name__
    menus_obj = FirstLayerMenu.objects.filter(url_name=func_name).first()
    firstmenus = model_to_dict(menus_obj).get("id")
    return render(request, 'public/config.html', {"table": table, "app": app, "firstmenus": firstmenus})


@login_required
def public_task(request):
    return render(request, 'public/task.html', {"table": table, "app": app})


@login_required
def public_test(request):
    return render(request, 'public/test.html')


@login_required
def public_func_search(request):
    data = request.POST
    search_key = data.get("search")
    from public.models import BusinessFunc
    result = BusinessFunc.objects.filter(name__contains=search_key)
    result = serializers.serialize("json", result)
    result_list = [item.get("fields") for item in json.loads(result)][:20]
    return JsonResponse(result_list, safe=False)


@login_required
def public_func_strict_search(request, func_str):
    from public.models import BusinessFunc
    result = BusinessFunc.objects.filter(expression=func_str).first()
    result = model_to_dict(result)
    return JsonResponse(result, safe=False)


@login_required
def retrieval_search(request):
    data = request.POST.get("data")

    params = parse_qs(data)  # 将a=1&b=2类型的数据转换为dict

    from public.models import Retrieval
    result = Retrieval.objects.all()
    result = serializers.serialize("json", result)
    result_list = [item.get("fields") for item in json.loads(result)]
    return JsonResponse(result_list, safe=False)


def public_request(request):
    data = request.POST.get("args")
    from urllib.parse import parse_qs
    params = parse_qs(data)  # 将a=1&b=2类型的数据转换为dict
    data = {key: params[key][0] for key in params}

    url = data.get("test_url")
    if url: url.strip()
    header = data.get("test_header")
    if header: header.strip()
    param = data.get("test_param")
    if param: param.strip()
    method = data.get("test_method")
    params_type = data.get("test_params_type")
    repeat_count = data.get("test_repeat_count")

    from utils.pubulic.RequestsUtil import _request
    if abs(int(repeat_count)) == 1 or abs(int(repeat_count)) == 0:
        result = _request(url=url, method=method, headers=header, data=param, params_type=params_type)
    else:
        duration = 0
        for i in range(abs(int(repeat_count))):
            result = _request(url=url, method=method, headers=header, data=param, params_type=params_type)
            duration += float(result["duration"])
            duration = round(duration, 2)
        result = {
            "code": 200,
            "duration": duration,
            "content": f"{abs(int(repeat_count))} requests have been sent!"
        }



    result.update(
        {
            "response_body":json.dumps(result["response_body"],indent=4,ensure_ascii=False) if result.get("response_body") else "",
            "response_headers":json.dumps(result["response_headers"],indent=4,ensure_ascii=False) if result.get("response_headers") else "",
            "request_headers":json.dumps(result["request_headers"],indent=4,ensure_ascii=False) if result.get("request_headers") else "",
            "request_body":json.dumps(result["request_body"],indent=4,ensure_ascii=False) if result.get("request_body") else "",
        }
    )
    return JsonResponse(result, safe=False)


@api_view(["POST"])
def public_dbconnect_tab1(request):
    data = request.POST.get("args")
    params = parse_qs(data)
    data = {key: params[key][0] for key in params}
    print(data)
    try:
        dbinfo = data.get("dbinfo").strip()
        sql = data.get("sql").strip()
        if sql.endswith(";"):
            sql = sql.strip(";")
        # if "limit" not in sql.lower():
        #     sql+= " limit 0,1000"
    except AttributeError:
        raise DefinedtError(code="10012", message="字段未填写完整")
    else:
        try:
            dbinfo = Dbinfo.objects.filter(name=dbinfo).first()
            dbinfo = {
                "dbhost": dbinfo.dbhost,
                "dbport": dbinfo.dbport,
                "dbname": dbinfo.dbname,
                "username": dbinfo.dbuser,
                "password": dbinfo.dbpassword
            }
            db = DBconnect(dbinfo, 'mysql', dict_flag=True)
            db.execute(sql)
            _data = db.query()
            db.close()
            if len(_data) > 0:
                column = list(_data[0].keys())
            else:
                column = None
        except Exception as e:
            raise DefaultError(code="10013", message=f"访问数据库失败,{str(e)}")
        else:
            result = {"data": _data, "column": column}
            raise DefinedSuccess(code="10010", result=result)


def public_dbconnect_tab2(request):
    code, message, _data = 200, "success", None
    data = request.POST.get("args")
    params = parse_qs(data)  # 将a=1&b=2类型的数据转换为dict
    data = {key: params[key][0] for key in params}
    try:
        dbinfo = data.get("dbinfo").strip()
        sql = data.get("sql").strip()
    except AttributeError:
        code = 10023
        message = "字段未填写完整！"
    else:
        try:
            dbinfo = Dbinfo.objects.filter(name=dbinfo).first()
            dbinfo = {
                "dbhost": dbinfo.dbhost,
                "dbport": dbinfo.dbport,
                "dbname": dbinfo.dbname,
                "username": dbinfo.dbuser,
                "password": dbinfo.dbpassword
            }
            db = DBconnect(dbinfo, "mysql", dict_flag=True)
            db.execute(sql)
            _data = db.query()
            db.close()
            _data = json.dumps(_data, indent=4, ensure_ascii=False)
        except Exception as e:
            code = 10014
            message = str(e)

    result = {}
    result.update({
        "code": code,
        "message": message,
        "data": _data
    })
    return JsonResponse(result, safe=False)


def public_dbconnect_tab3(request):
    code, message, _data = 200, "success", None
    data = request.POST.get("args")
    params = parse_qs(data)  # 将a=1&b=2类型的数据转换为dict
    data = {key: params[key][0] for key in params}
    try:
        dbinfo = data.get("dbinfo").strip()
        field_list = data.get("field_list").split(";")
        sql = data.get("sql").strip()
    except AttributeError:
        code = 10023
        message = "字段未填写完整！"
    else:

        try:
            dbinfo = Dbinfo.objects.filter(name=dbinfo).first()
            dbinfo = {
                "dbhost": dbinfo.dbhost,
                "dbport": dbinfo.dbport,
                "dbname": dbinfo.dbname,
                "username": dbinfo.dbuser,
                "password": dbinfo.dbpassword
            }
            db = DBconnect(dbinfo, "mysql")
            db.execute(sql)
            _data = db.output_selfdefined_dict(sql, param_dict=None, field_list=field_list)
            _data = json.dumps(_data, indent=4, ensure_ascii=False)
            db.close()
        except Exception as e:
            code = 10015
            message = str(e)
    result = {}
    result.update({
        "code": code,
        "message": message,
        "data": _data
    })
    return JsonResponse(result, safe=False)


def public_log_tab1(request):
    code, message, _data = 200, "success", None
    data = request.POST.get("args")
    params = parse_qs(data)  # 将a=1&b=2类型的数据转换为dict
    data = {key: params[key][0] for key in params}
    try:
        serverinfo = data.get("serverinfo").strip()
        order = data.get("order").strip()
    except AttributeError:
        code = 10023
        message = "字段未填写完整！"
    else:
        try:
            serverinfo = LogServerinfo.objects.filter(name=serverinfo).first()
            serverinfo = {
                "hostname": serverinfo.logserver,
                "port": serverinfo.logport,
                "username": serverinfo.logname,
                "password": serverinfo.logpwd
            }
            sshobj = MyParamiko(serverinfo)
            _data = sshobj.run_cmd(order)
            sshobj.close()
        except Exception as e:
            code = 10015
            message = str(e)
    result = {}
    result.update({
        "code": code,
        "message": message,
        "data": _data
    })
    return JsonResponse(result, safe=False)


def public_compare_tab1(request):
    code, message, path = 200, "success", None
    data = request.POST.get("args")
    params = parse_qs(data)
    data = {key: params[key][0] for key in params}
    expect = data.get("expect").strip()
    actual = data.get("actual").strip()
    black_list = data.get("black_list")
    if black_list:
        black_list = black_list.strip().split(';')
    skipped_list = data.get("skipped_list")
    if skipped_list:
        skipped_list = skipped_list.strip().split(';')
    try:
        expect = ast.literal_eval(expect)
        actual = ast.literal_eval(actual)
    except ValueError:
        code, message = 10021, "数据格式错误，应为字典或json形式"
    else:
        if isinstance(expect, dict) and isinstance(actual, dict):
            obj = GenerateCompareReport()
            data = [expect, actual]
            field_result = obj._generateCNHtml(data, black_list=black_list, skipped_list=skipped_list)
            path = obj._generateHtml("两组数据对比结果", field_result)
        else:
            code, message = 10022, "数据格式错误，应为字典"
    result = {}
    result.update({
        "code": code,
        "message": message,
        "data": path
    })
    return JsonResponse(result, safe=False)


def public_json_format(request):
    code, message, data = 200, "success", None
    data = request.POST.get("args")
    params = parse_qs(data)  # 将a=1&b=2类型的数据转换为dict
    data = {key: params[key][0] for key in params}
    data = data.get("json_data").strip()
    try:
        data = ast.literal_eval(data)
        if isinstance(data, dict):
            data = json.dumps(data, indent=4, ensure_ascii=False)
    except Exception:
        code = 11521
        message = "源数据格式错误！"

    result = {}
    result.update({
        "code": code,
        "message": message,
        "data": data
    })
    return JsonResponse(result, safe=False)


def display_process_log(request):
    id = request.POST.get("id")
    from public.models import StepLog
    log_info = model_to_dict(StepLog.objects.filter(id=id).first())
    if isinstance(log_info["origin"],dict):
        log_info["origin"]=json.dumps(log_info["origin"], indent=4, ensure_ascii=False)
    if isinstance(log_info["detail"],dict):
        log_info["detail"] = json.dumps(log_info["detail"], indent=4, ensure_ascii=False)
    return JsonResponse(log_info, safe=False)


def todo(request):
    test2 = [{"text": "ceshi", "done": False, "id": 1}]
    return render(request, "public/todo.html", {"data": json.dumps(test2)})
