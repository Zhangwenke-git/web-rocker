from django.shortcuts import render, redirect
from django.http import JsonResponse
from utils.pubulic.logger import Logger
from core import forms

logger = Logger("core base_admin")


class AdminRegisterException(Exception):  # 自定义异常
    def __init__(self, msg):
        self.message = msg


class BaseAdmin(object):  # 自定义方法
    list_display = ()
    list_per_page = 10
    list_filter = ()
    search_fields = ()
    ordering = None
    readonly_fields = ()
    readonly_table = False
    filter_horizontal = []
    modelform_exclude_fields = []  # 排除不显示
    color_fields = {}
    expand_flag = False
    wrap_flag = False  # 决定表格中的数据是否换行
    check_flag = False
    right_flag = False
    actions = []
    default_actions = ["delete_selected", "valid_selected","invalid_selected",]
    defined_add_link=False
    process_bar = []
    import_setting = False
    list_editable = []


    def delete_selected(self, request, queryset):
        app_name = self.model._meta.app_label  # app名
        model_name = self.model._meta.model_name  # 表名
        objs = queryset  # 类对象
        action = request._admin_action
        logger.info(f"Prepare to execute operation: [{action}]")
        if request.POST.get('delete_confirm') == 'yes':  # {#table_delete.html#}
            queryset.delete()
            return redirect('/%s/%s/' % (app_name, model_name))
        selected_ids = ','.join([str(i.id) for i in queryset])
        logger.debug(f'The selected ids are: [{selected_ids}]')
        return render(request, "public/table_data_delete.html", locals())  # 返回删除页

    delete_selected.short_description = "批量删除"


    def valid_selected(self,request,queryset):
        app_name = self.model._meta.app_label  # app名
        model_name = self.model._meta.model_name  # 表名
        admin_obj = site.registered_sites[app_name][model_name]
        selected_ids =[int(i.id) for i in queryset]
        for selected_id in selected_ids:
            admin_obj.model.objects.filter(id=selected_id).update(statue=1)
        return redirect("/%s/%s/" % (app_name, model_name))

    valid_selected.short_description = "批量有效"

    def invalid_selected(self, request, queryset):
        app_name = self.model._meta.app_label  # app名
        model_name = self.model._meta.model_name  # 表名
        admin_obj = site.registered_sites[app_name][model_name]
        selected_ids = [int(i.id) for i in queryset]
        for selected_id in selected_ids:
            admin_obj.model.objects.filter(id=selected_id).update(statue=0)
        return redirect("/%s/%s/" % (app_name, model_name))

    invalid_selected.short_description = "批量废弃"

    def default_form_validation(self, request):
        pass


class AdminSite(object):
    def __init__(self):
        self.registered_sites = {}

    def register(self, model, admin_class=None):  # 默认值None 使用 BaseAdmin
        app_name = model._meta.app_label  # 用内置方法获取 APP名字 （myapp）
        model_name = model._meta.model_name  # 用内置方法获取 表名  (User)
        #logger.debug(f"The application and model name are [{app_name, model_name}]")
        if app_name not in self.registered_sites:
            self.registered_sites[app_name] = {}  # 创建  myapp={}
        if model_name in self.registered_sites[app_name]:
            logger.error("App [%s] > model [%s] has already registered!" % (app_name, model_name))
            raise AdminRegisterException(
                "App [%s] > model [%s] has already registered!" % (app_name, model_name))  # 自定义异常
        if not admin_class:
            admin_class = BaseAdmin  # 默认值None 使用class BaseAdmin
        admin_obj = admin_class()
        admin_obj.model = model
        self.registered_sites[app_name][model_name] = admin_obj

site = AdminSite()
