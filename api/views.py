import json, re
import ast
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
from public.models import FirstLayerMenu
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
                            scenario_dict = {}
                            case_expect_item["module"] = case_copy.pop("testsuit__module")
                            case_expect_item["class_title"] = case_copy.pop("testsuit__class_title")
                            case_expect_item["case"] = case_copy.pop("testsuit__testcase__case")
                            case_expect_item["case_title"] = case_copy.pop("testsuit__testcase__case_title")
                            case_expect_item["case_description"] = case_copy.pop("testsuit__testcase__case_description")
                            case_expect_item["templates_name"] = case_copy.pop("testsuit__testcase__templates__name")
                            case_expect_item["url"] = case_copy.pop("testsuit__testcase__templates__url")
                            case_expect_item["method"] = case_copy.pop("testsuit__testcase__templates__method")
                            case_expect_item["header"] = eval(
                                str(case_copy.pop("testsuit__testcase__templates__header")))
                            case_expect_item["data"] = eval(str(case_copy.pop("testsuit__testcase__templates__data")))

                            param_list = eval(case_copy["testsuit__testcase__scenario__parameter"])
                            parameter = _multiDictMerge(param_list)
                            validator_list = eval(case_copy["testsuit__testcase__scenario__validator"])
                            validator = _multiDictMerge(validator_list)

                            scenario_dict.update({
                                "parameter": parameter,
                                "name": case_copy["testsuit__testcase__scenario__scenario"],
                                "validator": validator

                            })
                            case_item_list.append(scenario_dict)

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
    return render(request, '403.html')


@login_required
def api_analytics(request):
    return render(request, 'api/analytics.html')


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
        field_list = comment.findall(case_template)
        fields = list(map(remove_character, field_list))
        fields = list(set(fields))

        func_pattern = r'\$\{.+?>'
        comment = re.compile(func_pattern, re.DOTALL)
        func_list = comment.findall(case_template)
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

        response = {"code": code, "message": message}
        return JsonResponse(response, safe=False)
    return render(request, 'api/scenario.html', locals())



@login_required
def check_template(request,app_name, model_name, template_id):
    admin_obj = site.registered_sites[app_name][model_name]
    obj = admin_obj.model.objects.get(id=template_id)
    test=model_to_dict(obj)
    test["data"] = json.loads(test["data"])
    if request.method == "GET":
        table_html = json2html.json2html.convert(test)
        table_html = table_html.replace('table border="1"','table class="table table-bordered text-wrap"').replace(
            '<tr>','<tr class="table">'
        ).replace('<th>','<th class="text-secondary">').replace('<td>{{','<td class="text-danger">{{').replace(
            '<td>${','<td class="text-success">${')
        return render(request,"api/template_check.html", {"data":mark_safe(table_html)})
