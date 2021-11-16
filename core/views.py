import json, datetime
import os

import random
import time
from core.exceptions import DefaultError, DefinedSuccess, DefinedtError
from rest_framework.decorators import api_view
from core.client import client
from utils.pubulic.FtpUtils import FTPHelper
from utils.pubulic.ReadConfig import ReadConfig
from config.path_config import base_dir
from django.db.models import Q
from django.forms import model_to_dict
from public.models import StepLog
from django.http import JsonResponse
from core import form
from django.shortcuts import render
from core.base_admin import site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from core.permissions import check_permission
from utils.pubulic.MyEncoder import encoder_render
from core.query import *
from core.parameter_ import PARAMETER


logger = Logger("core view")


def get_queryset_search_result(request, queryset, admin_obj):
    search_key = request.GET.get("_q", "")  # 取定义名,默认为空
    q_obj = Q()  # 多条件搜索 #from django.db.models import Q
    q_obj.connector = "OR"  # or/或 条件

    for column in admin_obj.search_fields:
        q_obj.children.append(("%s__contains" % column, search_key))  # 运态添加多个条件
    res = queryset.filter(q_obj)  # 对数据库进行条件搜索
    return res, admin_obj.search_fields  # 返回结果


def filter_querysets(request, queryset):
    condtions = {}
    for k, v in request.GET.items():  # 不需要空的,判断是否为空
        if k in ("page", "_o", "_q"): continue
        if k !="csrfmiddlewaretoken":
            if v: condtions[k] = v
    query_res = queryset.filter(**condtions)
    return query_res, condtions


@login_required
@check_permission
def batch_update(request, editable_data, admin_obj):
    errors = []  # 错误信息
    for row_data in editable_data:
        obj_id = row_data.get('id')  # 获取这行ID号
        try:
            if obj_id:
                obj = admin_obj.model.objects.get(id=obj_id)  # 获取编辑的ID
                model_form = form.create_form(admin_obj.model, list(row_data.keys()),
                                              admin_obj, request=request, partial_update=True)  # 进行数据验证处理
                form_obj = model_form(instance=obj, data=row_data)  # 编辑的ID #验证的内容
                if form_obj.is_valid():  # 验证通过
                    form_obj.save()  # 保存新内容
                else:
                    errors.append([form_obj.errors, obj])  # 添加错误信息
        except KeyboardInterrupt as e:
            return False, [e, obj]
    if errors:
        return False, errors
    return True, []


def get_orderby(request, queryset, admin_obj):
    orderby_key = request.GET.get("_o")
    if orderby_key:  # 有获取到字段
        query_res = queryset.order_by(orderby_key.strip())  # .strip()默认删除空白符（包括'\n', '\r',  '\t',  ' ')
    else:
        if admin_obj.ordering:
            query_res = queryset.order_by("%s" % admin_obj.ordering)
        else:
            query_res = queryset.order_by('-id')  # 默认倒序
    return query_res


@check_permission
@login_required
def table_data_list(request, app_name, model_name):
    admin_obj = site.registered_sites[app_name][model_name]

    if request.method == "POST":  # 批量操作
        action = request.POST.get("action_select")  # 要调用的自定制功能函数
        selected_ids = request.POST.get("selected_ids")  # 前端提交的数据
        editable_data = request.POST.get("editable_data")  # 获取前端可编辑的数据
        if editable_data:  # for list editable
            editable_data = json.loads(editable_data)  # 进行转换数据
            res_state, errors = batch_update(request, editable_data, admin_obj)  # 进行部分更新操作
        else:
            if selected_ids:
                selected_objs = admin_obj.model.objects.filter(id__in=selected_ids.split(','))  # 返回之前所选中的条件
            else:
                raise KeyError('No selection object!')
            if hasattr(admin_obj, action):
                action_func = getattr(admin_obj, action)  # 如果admin_obj 对象中有属性action 则打印self.action的值，否则打印'not find'
                request._admin_action = action  # 添加action内容
            return action_func(request, selected_objs)

    admin_obj.querysets = admin_obj.model.objects.all()  # 取数据 传到 前端
    obj_list = admin_obj.model.objects.all().order_by('-id')
    queryset, condtions = filter_querysets(request, obj_list)  # base_admin   # 调用条件过滤
    queryset, search_fields = get_queryset_search_result(request, queryset, admin_obj)  ##搜索后

    cn_search_field_name = [admin_obj.model._meta.get_field(field).verbose_name for field in search_fields]
    cn_search_field_name = "or".join(cn_search_field_name)

    count = queryset.count()
    blank_table = True if count == 0 else False
    width = len(admin_obj.list_display) + 1

    wrap_flag = "text-wrap" if admin_obj.wrap_flag else "text-nowrap"

    sorted_queryset = get_orderby(request, queryset, admin_obj)
    paginator = Paginator(sorted_queryset, admin_obj.list_per_page)
    page = request.GET.get('page')

    try:
        objs = paginator.page(page)  # 当前的页面的数据
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)

    admin_obj.querysets = objs  # base_admin
    admin_obj.filter_condtions = condtions

    return render(request, "public/table_data_list.html", locals())


from core import forms


@check_permission
@login_required
def table_data_update(request, app_name, model_name, obj_id):
    request.POST._mutable = True
    request.GET._mutable = True  # 为了让request中的queryDict变成可编辑可更改

    admin_obj = site.registered_sites[app_name][model_name]
    model_form = forms.CreateModelForm(request, admin_obj=admin_obj)
    obj = admin_obj.model.objects.get(id=obj_id)
    operate_data = model_to_dict(admin_obj.model.objects.filter(id=obj_id).first())

    if request.method == "GET":
        obj_form = model_form(instance=obj)
    elif request.method == "POST":
        if len(request.FILES) != 0:
            logger.debug(f"There is a file [{request.FILES}] to be uploaded,it is a update action!")
            obj_form = model_form(request.POST, request.FILES, instance=obj)
        else:
            obj_form = model_form(instance=obj, data=request.POST)

        for k, v in obj_form.base_fields.items():
            if v.widget.attrs.get("data-type") == "date":
                date_ = obj_form.data[k]
                try:
                    date_ = datetime.datetime.strptime(date_, '%d %B, %Y').strftime('%Y-%m-%d')  # 将英文日期转换为数字日期
                except ValueError:
                    pass
                finally:
                    obj_form.data.update({k: date_})

        if obj_form.is_valid():
            try:
                obj_form.save()
            except Exception as e:
                error_message = f"{e}"
            else:
                log_data = model_to_dict(admin_obj.model.objects.filter(id=obj_id).first())
                log_data = encoder_render(log_data)
                operate_data = encoder_render(operate_data)
                StepLog.objects.create(user=request.user.user_id,
                                       action="更新",
                                       model_name="%s-%s" % (app_name, model_name),
                                       detail=log_data,
                                       origin=operate_data
                                       )

                return redirect("/%s/%s/" % (app_name, model_name))
    return render(request, "public/table_data_update.html", locals())


from django.shortcuts import redirect


@check_permission
@login_required
def table_data_add(request, app_name, model_name):
    request.POST._mutable = True
    request.GET._mutable = True
    admin_obj = site.registered_sites[app_name][model_name]  # 获取表对象
    admin_obj.is_add_form = True  # 必须在下一句创建Model_form代码的前面
    model_form = forms.CreateModelForm(request, admin_obj=admin_obj)  ##modelform 生成表单 加验证

    if request.method == "GET":
        obj_form = model_form()
    elif request.method == "POST":
        if len(request.FILES) != 0:
            logger.debug(f"There is a file [{request.FILES}] to be uploaded!")
            obj_form = model_form(request.POST, request.FILES)
        else:
            obj_form = model_form(request.POST)

        password = request.POST.get('password')
        user_id = request.POST.get('user_id')

        for k, v in obj_form.base_fields.items():
            if v.widget.attrs.get("data-type") == "date":
                date_ = obj_form.data[k]
                try:
                    date_ = datetime.datetime.strptime(date_, '%d %B, %Y').strftime('%Y-%m-%d')  # 将英文日期转换为数字日期
                except ValueError:
                    pass
                finally:
                    obj_form.data.update({k: date_})

        if obj_form.is_valid():
            try:
                if len(request.FILES) != 0:
                    upload_file = obj_form.cleaned_data["upload"]
                    upload_file_name = obj_form.cleaned_data["upload"].name
                    logger.debug(f"The file is: {upload_file}")
                obj_form.save()
            except Exception as e:
                logger.error(f"Fail to upload the file,error as follows: {str(e)}")
                error_message = f"{e}"
                return render(request, "public/table_data_add.html", locals())
            else:
                log_data = model_to_dict(admin_obj.model.objects.all().last())
                log_data=encoder_render(log_data)
                StepLog.objects.create(user=request.user.user_id,
                                       action="新增",
                                       model_name="%s-%s" % (app_name, model_name),
                                       detail=log_data
                                       )

        if not obj_form.errors:  # 没有错误返回原来的页面
            if user_id:
                obj = admin_obj.model.objects.filter(user_id=user_id).first()  # 对象
                obj.set_password(password)  # 加密
            try:
                obj.save()  # 表单验证通过保存
            except Exception as e:
                return redirect("/%s/%s/" % (app_name, model_name))

            return redirect("/%s/%s/" % (app_name, model_name))

    return render(request, "public/table_data_add.html", locals())


@check_permission
@login_required
def table_data_delete(request, app_name, model_name, obj_id):
    admin_obj = site.registered_sites[app_name][model_name]  # 表类
    objs = admin_obj.model.objects.filter(id=obj_id)  # 类的对象

    operate_data = model_to_dict(admin_obj.model.objects.filter(id=obj_id).first())
    operate_data=encoder_render(operate_data)
    if admin_obj.readonly_table:
        errors = {'Locked table': 'The table:<%s>,has been locked,and can not be deleted!' % model_name}
    else:
        errors = {}
    if request.method == 'POST':
        if not admin_obj.readonly_table:
            objs.delete()  # 删除
            StepLog.objects.create(user=request.user.user_id,
                                   action="删除",
                                   model_name="%s-%s" % (app_name, model_name),
                                   origin=operate_data
                                   )

            return redirect("/%s/%s/" % (app_name, model_name))  # 转到列表页面
    return render(request, "public/table_data_delete.html", locals())  # locals 返回一个包含当前范围的局部变量字典。


@login_required
def password_reset(request, app_name, model_name, obj_id):
    admin_obj = site.registered_sites[app_name][model_name]  # 表类
    obj = admin_obj.model.objects.get(id=obj_id)  # 类表的对象

    errors = {}  # 错误提示
    if request.method == 'POST':
        _password1 = request.POST.get('password1')  # 获取页面输入的值
        _password2 = request.POST.get('password2')  # 获取页面输入的值
        if _password1 == _password2:
            if len(_password1) > 7:
                obj.set_password(_password1)  # 继承Django方法 #加密
                obj.save()  # 保存
                return redirect(request.path.rstrip('password/') + ('/update/'))  # 替换URL名
            else:
                errors['password_too_short'] = 'At least 8 characters!'
        else:
            errors['invalid_password'] = 'Not the same password!'  # 密码不一致

    return render(request, "common/password_reset.html", locals())


@login_required
def quick_password_reset(request):
    errors = {
        "code": 2003,
        "message": None
    }  # 错误提示
    if request.method == 'POST':
        id = request.POST.get("id")
        from public.models import UserProfile
        user_info_obj = UserProfile.objects.filter(id=id).first()
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-,."
        salt = [random.choice(seed) for i in range(10)]
        salt = ''.join(salt)

        user_info = {
            "account": user_info_obj.user_id,
            "password": salt
        }

        try:
            user_info_obj.set_password(salt)
            user_info_obj.save()
        except Exception as e:
            errors["message"] = str(e)
        else:
            errors["code"] = 200
            errors["message"] = user_info
    return JsonResponse(errors, safe=False)


@login_required
def password_add(request, app_name, model_name):
    return redirect("/%s/%s/" % (app_name, model_name))


@login_required
def api_execute(request, app_name, model_name, selected_id):
    admin_obj = site.registered_sites[app_name][model_name]

    _dict={}
    for instance in admin_obj.querysets:
        if str(instance.id) == str(selected_id):
            selected_obj = instance
            item= model_to_dict(selected_obj)
    return render(request, "api/execute.html", locals())


parameter_ = PARAMETER()

@login_required
def ajax_api_execute(request):
    data = request.POST
    model_name = data.get("model")
    selected_ids = data.get("selected").split(",")
    selected_id = data.get("selected_id")

    parameter_.process_bar= random.randint(4,8)
    parameter_.process_message= "开始搜集用例..."
    time.sleep(1)

    if model_name == "testsuit":
        data = single_query_testsuit_data(selected_ids)
    elif model_name == "testcase":
        data = single_query_testcase_data(selected_id, selected_ids)
    elif model_name == "apiproject":
        data = single_query_project_data(selected_ids)

    parameter_.process_bar= random.randint(9,15)
    parameter_.process_message= "用例搜集完成！"
    time.sleep(1)

    parameter_.process_bar=random.randint(20,35)
    parameter_.process_message= "开始执行用例"
    time.sleep(1)

    flag, remote_dir = client(data)

    parameter_.process_bar=random.randint(36,70)
    parameter_.process_message= "用例执行完成，并完成测试报告上传！"
    time.sleep(1)

    if flag and len(remote_dir) != 0:
        _time = os.path.basename(os.path.dirname(remote_dir))
        report = os.path.join(base_dir, "static/report_temp")

        if os.path.exists(report):
            pass
        else:
            os.makedirs(report)

        ip, port, user, pwd = ReadConfig.getFtp()
        ftp = FTPHelper(ip=ip, password=pwd, port=port, username=user)

        parameter_.process_bar = random.randint(71,80)
        parameter_.process_message = "开始从FTP下载测试报告..."
        time.sleep(1)

        ftp.download_dir(report, remote_dir)
        ftp.close()

        parameter_.process_bar = random.randint(81,87)
        parameter_.process_message = "报告下载完成！"
        time.sleep(1)

        parameter_.process_bar = random.randint(88,91)
        parameter_.process_message = "开始读取报告..."
        time.sleep(1)
        local = os.path.join(report, "ant")

        for root, dirs, files in os.walk(local):
            for file in files:
                if file.endswith(".html"):
                    html_file = os.path.join(local, file)
                    html_file = os.path.join("\\", html_file.replace(base_dir, ""))

        parameter_.process_bar = random.randint(92,94)
        parameter_.process_message = "报告读取成功！"
        time.sleep(1)

        parameter_.process_bar = 99
        parameter_.process_message = "测试报告展示"
        time.sleep(1)

    return JsonResponse({"success":True,"data":html_file})

@login_required
def show_progress(request):
    submit_progress = request.POST.get("submit_progress")
    if submit_progress == "100%":
        parameter_.process_bar = 3
        parameter_.process_message = "准备就绪..."

    process_bar = parameter_.process_bar
    process_message = parameter_.process_message

    try:
        return JsonResponse({"process_bar":process_bar,"process_message":process_message}, safe=False)
    except Exception:
        logger.debug("error")

