import json, re
import ast
from collections import defaultdict
from datetime import datetime
from functools import reduce

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators import csrf
from api.models import *
from core.app_load import app_loader
from utils.pubulic.logger import Logger
from core.base_admin import site
from django.contrib.auth.decorators import login_required
from public.models import FirstLayerMenu, StepLog
from core.permissions import check_permission
from urllib.parse import parse_qs, urlparse
from copy import deepcopy
import json2html

global false, null, true
false = False
true = True
null = ''


def _mergeDict(dict1, dict2):
    """
    :function:将两个字典重新组合成一个
    :param dict1:
    :param dict2:
    :return:
    """
    dictMerged = dict1.copy()
    dictMerged.update(dict2)
    return dictMerged


def _multiDictMerge(dictList):
    """
    :function:将多个字典融合，融合过程是一个迭代的过程，dict1和dict2融合为一个新的dict1_2,dict1_2再与dict3融合，生成最终的一个dict
    :param dictList: {dict1,dict2,dict3},reduce为python的高阶函数，效果就逐层迭代，返回最终迭代的结果
    :return:
    """
    newDict = reduce(_mergeDict, dictList)
    return newDict


app_loader("api")
logger = Logger("api view")

# Create your views here.
table = site.registered_sites.get("api")
app = 'api'


def get_project_case():
    """
    func:获取所有有效的测试项目，用例集，用例和场景数据
    @return:
    """
    api_project_list = ApiProject.objects.values_list("name", flat=True)
    project_dict_list = []
    for project_name in api_project_list:
        project_dict = dict()
        item = ApiProject.objects.filter(name=project_name).values("testsuit__module",
                                                                   "testsuit__class_title",
                                                                   "testsuit__testcase__case",
                                                                   "testsuit__testcase__case_title",
                                                                   "testsuit__testcase__case_description",
                                                                   "testsuit__testcase__templates__name",
                                                                   "testsuit__testcase__templates__url",
                                                                   "testsuit__testcase__templates__method",
                                                                   "testsuit__testcase__templates__method",
                                                                   "testsuit__testcase__templates__header",
                                                                   "testsuit__testcase__templates__data",
                                                                   "testsuit__testcase__scenario__scenario",
                                                                   "testsuit__testcase__scenario__parameter",
                                                                   "testsuit__testcase__scenario__validator", )
        item = [i for i in item]
        project_dict[project_name] = item
        project_dict_list.append(project_dict)
    for project_dict in project_dict_list:
        for project, suits in project_dict.items():
            suit_name_list = [suit.get("testsuit__module") for suit in suits]
            suit_name_list = list(filter(None, list(set(suit_name_list))))  # 将每个项目下的用例集合进行去重并删除为None的值
            if len(suit_name_list) == 0:
                project_dict_list.remove(project_dict)
    for project_dict in project_dict_list:
        for project, suits in project_dict.items():
            case_name_list = []
            for suit in suits:
                case_name_list.append(suit.get("testsuit__testcase__case"))
                case_name_list = list(filter(None, list(set(case_name_list))))
                if len(case_name_list) == 0 or not suit.get(
                        "testsuit__testcase__scenario__scenario"):  # 删除用例集下没有测试用例或者测试用例没有模板或者没有场景的的数据
                    suits.remove(suit)
    logger.debug(f"修剪后的全部项目信息:{project_dict_list}")
    all_project = []
    for project_dict in project_dict_list:
        project_expect_list = []
        project_expect_dict = dict()
        for project, suits in project_dict.items():

            suits_expect_list = []
            suit_name_list = [suit.get("testsuit__module") for suit in suits]
            suit_name_list = list(set(suit_name_list))

            print(f"该项目{project}下的测试用例集合：{suit_name_list}")

            for suit_name in suit_name_list:
                suit_expect_dict = dict()
                suit_item_list = []
                for suit in suits:
                    if suit["testsuit__module"] == suit_name:
                        suit_copy = deepcopy(suit)
                        # del suit_copy["testsuit__module"]
                        # del suit_copy["testsuit__class_title"]
                        suit_item_list.append(suit_copy)

                case_name_list = [case["testsuit__testcase__case"] for case in suit_item_list]
                case_name_list = list(set(case_name_list))

                case_expect_list = []
                for case_name in case_name_list:
                    case_expect_item = dict()
                    case_item_list = []
                    for case in suit_item_list:
                        if case["testsuit__testcase__case"] == case_name:
                            case_copy = deepcopy(case)
                            scenario_list = []
                            case_expect_item["module"] = case_copy.pop("testsuit__module")
                            case_expect_item["class_title"] = case_copy.pop("testsuit__class_title")
                            case_expect_item["case"] = case_copy.pop("testsuit__testcase__case")
                            case_expect_item["case_title"] = case_copy.pop("testsuit__testcase__case_title")
                            case_expect_item["case_description"] = case_copy.pop("testsuit__testcase__case_description")
                            case_expect_item["templates_name"] = case_copy.pop("testsuit__testcase__templates__name")
                            case_expect_item["url"] = case_copy.pop("testsuit__testcase__templates__url")
                            case_expect_item["method"] = case_copy.pop("testsuit__testcase__templates__method")
                            case_expect_item["header"] = case_copy.pop("testsuit__testcase__templates__header")
                            case_expect_item["data"] = case_copy.pop("testsuit__testcase__templates__data")

                            param_list = case_copy["testsuit__testcase__scenario__parameter"]
                            parameter = _multiDictMerge(param_list)
                            validator_list = case_copy["testsuit__testcase__scenario__validator"]
                            validator = _multiDictMerge(validator_list)

                            scenario_list=[
                                parameter,
                                case_copy["testsuit__testcase__scenario__scenario"],
                                validator

                            ]
                            case_item_list.append(scenario_list)

                    case_expect_item["scenarios"] = case_item_list
                    case_expect_list.append(case_expect_item)
                suit_expect_dict[suit_name] = case_expect_list

                suits_expect_list.append(suit_expect_dict)

            project_expect_dict[project] = suits_expect_list
            project_expect_list.append(project_expect_dict)

        all_project.append(project_expect_list[0])
    logger.debug(f"汇总后的全部项目信息为：{all_project}")
    return all_project

@login_required
def api_overview(request):
    func_name = api_overview.__name__
    menus_obj = FirstLayerMenu.objects.filter(url_name=func_name).first()
    firstmenus = model_to_dict(menus_obj).get("id")
    get_project_case()
    return render(request, 'api/overview.html', {"table": table, "app": app, "firstmenus": firstmenus})


@login_required
def api_report(request):
    return render(request, 'error/403.html')


@login_required
def api_analytics(request):
    title = "2010 ~ 2016 年太阳能行业就业人员发展情况"
    serias =  [{
				"name": '安装，实施人员',
				"data": [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]
		},
        {
            "name": '工人',
            "data": [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
        }
    ]

    return render(request, 'api/analytics.html',locals())

from datetime import datetime
from datetime import timedelta
from utils.pubulic.DBUtil import DBconnect


@login_required
def project_graph_ajax(request):

    db = DBconnect(
        {
            "dbhost": "127.0.0.1",
            "dbport": "3306",
            "dbname": "django",
            "username": "root",
            "password": null,

        }, type="mysql", dict_flag=True
    )
    db.execute('''
SELECT project,create_date,COUNT(CASE WHEN result ='Passed' THEN 1 END)/COUNT(*) AS rate FROM `api_executionrecord` WHERE  DATE_SUB(CURDATE(), INTERVAL 6 DAY) <= DATE(`create_date`) GROUP BY `project`,`create_date`;    ''')
    data = db.query()
    db.execute('''
SELECT project FROM `api_executionrecord` WHERE  DATE_SUB(CURDATE(), INTERVAL 6 DAY) <= DATE(`create_date`) GROUP BY `project`''')
    projects = db.query()
    db.close()
    projects = [pro["project"] for pro in projects]
    cur = datetime.now().date()
    last_seven = [cur-timedelta(days=d) for d in range(7)]
    last_seven.reverse()
    series = []
    for pro in projects:
        serie = dict()
        project_data = []
        for temp in data:
            if temp["project"] == pro:
                project_data.append((temp["create_date"],float(round(temp["rate"],2))))
        rate_list = [0,0,0,0,0,0,0]
        project_sorted = sorted(project_data,key=lambda x:x[0])

        for da_ in project_sorted:
            if da_[0] in last_seven:
                index = last_seven.index(da_[0])
                rate_list[index]=da_[1]
        serie["name"]=pro
        serie["data"]=rate_list
        series.append(serie)
    response = {
        "code":200,
        "success":True,
        "result":{
            "title":"API项目最近一周成功率",
            "subtitle":"仅统计最新的项目成功率",
            "yAxis":"成功率",
            "xAxis": last_seven,
            "series":series

        }
    }
    return JsonResponse(response)



@login_required
def through_graph_ajax(request):
    db = DBconnect(
        {
            "dbhost": "127.0.0.1",
            "dbport": "3306",
            "dbname": "django",
            "username": "root",
            "password": null,

        }, type="mysql", dict_flag=True
    )
    db.execute('''
SELECT MONTH(create_time) AS monthNo,COUNT(*) AS through FROM `api_executionrecord` WHERE YEAR(create_time) = DATE_FORMAT(NOW(),'%Y') GROUP BY MONTH(create_time);
 ''')
    data = db.query()
    db.close()
    through = [0,0,0,0,0,0,0,0,0,0,0,0]
    for index,value in enumerate(through):
        for da_ in data:
            if da_["monthNo"] == index+1:
                through[index]=da_["through"]

    response = {
        "code": 200,
        "success": True,
        "result": {
            "title": "每月用例执行量",
            "xAxis":["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"],
            "series": through

        }
    }
    return JsonResponse(response)


@login_required
def current_month_graph_ajax(request):
    db = DBconnect(
        {
            "dbhost": "127.0.0.1",
            "dbport": "3306",
            "dbname": "django",
            "username": "root",
            "password": null,

        }, type="mysql", dict_flag=True
    )
    db.execute('''
SELECT COUNT(*) as y,project as name FROM `api_executionrecord` WHERE YEAR (create_time) = DATE_FORMAT(NOW(),'%Y-%m') GROUP BY project;
     ''')
    data = db.query()
    db.close()
    total = sum([d["y"] for d in data])
    for d in data:
        d["y"] = float(round(d["y"]/total,2))
    response = {
        "code": 200,
        "success": True,
        "result": {
            "title": "本月执行项目占比",
            "series": data

        }
    }
    return JsonResponse(response)


@login_required
def case_info_graph_ajax(request):
    from api.models import Scenario

    data = Scenario.objects.all().values(
       "test_case__test_suit__project__name","test_case__test_suit__module", "test_case__case","scenario"
    )


    projects = list(set([item["test_case__test_suit__project__name"] for item in data]))

    suits_result = []
    scenarios_result =[]
    for project in projects:
        cases = []
        for item in data:
            if project == item["test_case__test_suit__project__name"]:
                cases.append(item)
                scenarios_count = len(cases)
        suites = list(set([i["test_case__test_suit__module"] for i in cases]))

        suites_count = len(suites)

        suits_result.append(suites_count)
        scenarios_result.append(scenarios_count)
    result = [
        {"name":"suites","data":suits_result},
        {"name":"scenarios","data":scenarios_result},
    ]


    response = {
        "code": 200,
        "success": True,
        "result": {
            "title": "API项目容量概况",
            "subtitle": "当日项目容量概况",
            "xAxis":projects,
            "series": result

        }
    }
    return JsonResponse(response)



@login_required
def display_param(request):
    def remove_character(string: str):
        character = ['$', '{', '}']
        for char_ in character:
            string = string.replace(char_, '')
        return string

    code, result, message, data = 200, None, "success", {}
    if request.method == "GET":
        case_id = request.GET.get("case_id")
        case_info = TestCase.objects.filter(id=case_id).first()
        case_template = case_info.templates.data
        filed_pattern = r'\{{(.+?)\}}'
        comment = re.compile(filed_pattern, re.DOTALL)
        field_list = comment.findall(json.dumps(case_template))
        fields = list(map(remove_character, field_list))
        fields = list(set(fields))

        func_pattern = r'\$\{.+?>'
        comment = re.compile(func_pattern, re.DOTALL)
        func_list = comment.findall(json.dumps(case_template))
        func = list(map(remove_character, func_list))
        fields = list(set(fields))
        func_dict_list = []
        for fun in func:
            func_dict = {}
            fun_list = fun.split("|")
            try:
                func_dict[fun_list[0]] = fun_list[1]
            except IndexError:
                raise NameError(f"The separative sign '|' in function string: [{fun_list[0]}] not found!")
            func_dict = {k: list(v.replace('<', '').replace('>', '').split(',')) for k, v in
                         func_dict.items()}  # 处理参数的中特殊字符，并转换成tuple格式
            func_dict_list.append(func_dict)

        for temp in func_dict_list:
            for k, v in temp.items():
                if v[0] == "":
                    temp.update({k: None})
                else:
                    pass

        data.update(
            {"code": code, "fields": fields, "message": message, "func": func_dict_list}
        )
        return JsonResponse(data, safe=False)


@login_required
def api_scenarios(request):
    case_list = TestCase.objects.all().values()
    code, message = 200, '数据录入成功！'
    if request.method == "POST":
        posted = request.POST.get("args")
        params = parse_qs(posted)
        if params.get("csrfmiddlewaretoken"): del params["csrfmiddlewaretoken"]

        def format_data(item):
            dict_ = {}
            if int(item[2]) == 2:
                dict_[item[0]] = int(item[1])
            elif int(item[2]) == 3:
                dict_[item[0]] = float(item[1])
            elif int(item[2]) == 4:
                dict_[item[0]] = ast.literal_eval(item[1])
            elif int(item[2]) == 5:
                dict_[item[0]] = ast.literal_eval(item[1])
            elif int(item[2]) == 6:
                if eval(item[1]) != True:
                    dict_[item[0]] = False
                else:
                    dict_[item[0]] = True
            elif int(item[2]) == 7:
                dict_[item[0]] = None
            elif int(item[2]) == 8:
                dict_[item[0]] = ""
            else:
                dict_[item[0]] = item[1]
            return dict_

        if params.get("parameter"):
            parameter = json.loads(params["parameter"][0])
        else:
            param_key = params.get("param_key")
            param_value = params.get("param_value")
            param_type = params.get("param_type")
            params_ = list(zip(param_key, param_value, param_type))
            parameter = list(map(format_data, params_))

        if params.get("validator"):
            expect = json.loads(params["validator"][0])
        else:
            expect_key = params.get("expect_key")
            expect_value = params.get("expect_value")
            expect_type = params.get("expect_type")
            expect_ = list(zip(expect_key, expect_value, expect_type))
            expect = list(map(format_data, expect_))

        rk_dict = {}
        rk_dict.update({
            'scenario': params.get('scenario')[0],
            'priority': int(params.get('priority')[0]),
            'test_case_id': int(params.get('test_case')[0]),
            'statue': int(params.get('statue')[0]),
            'parameter': parameter,
            'validator': expect,
            'create_time': datetime.time()

        })
        logger.debug(f"场景入库信息：{rk_dict}")
        try:
            Scenario.objects.create(**rk_dict)
        except Exception as e:
            logger.error(f"该条数据入库失败，原因：{e}")
            code = 10013
            message = f"该条数据入库失败，原因：{e}"
        else:
            log_data = model_to_dict(Scenario.objects.all().first())
            StepLog.objects.create(user=request.user.user_id,
                                   action="新增",
                                   model_name="%s-%s" % ("api", "scenario"),
                                   detail=log_data
                                   )
        response = {"code": code, "message": message}
        return JsonResponse(response, safe=False)
    return render(request, 'api/scenario.html', locals())



@login_required
def check_template(request,app_name, model_name, template_id):
    admin_obj = site.registered_sites[app_name][model_name]
    obj = admin_obj.model.objects.filter(id=template_id).first()
    template_str=model_to_dict(obj)

    if request.method == "GET":
        table_html = json2html.json2html.convert(template_str)
        table_html = table_html.replace('table border="1"','table class="table table-bordered text-wrap"').replace(
            '<tr>','<tr class="table">'
        ).replace('<th>','<th class="text-secondary">').replace('<td>{{','<td class="text-danger">{{').replace(
            '<td>${','<td class="text-success">${')
        return render(request,"api/template_check.html", {"data":mark_safe(table_html)})
