from django.shortcuts import render, redirect
from core.base_admin import site, BaseAdmin
from django.forms import ValidationError
from public.models import *
from utils.pubulic.logger import Logger

logger = Logger("api_admin")


class UserProfileAdmin(BaseAdmin):
    list_display = (
        "id","upload","sex", "email", "name", "user_id", "is_active", "is_superuser", "role", "groups", "reset", "last_login",)
    # list_editable = ["email","name","is_active"] 添加上去后就会修改报错，todo:bug
    color_fields = {
        "is_active": {
            "否": "danger",
            "是": "success",
        },
        "is_superuser": {
            "否": "dark",
            "是": "success",
        },
    }
    readonly_fields = ("password",)
    modelform_exclude_fields = ['last_login']  # 排除#不显示
    # filter_horizontal = ["groups", "user_permissions", ]

    def role(self, obj):
        return [a.rolename for a in obj.role.all()]  # 多对多关系的时候，在list_display展示之用,函数名称需要和model中的名称保持一致

    role.display_name = "角色"

    def groups(self, obj):
        return [a.name for a in obj.groups.all()]

    groups.display_name = "权限组"

    def reset(self):
        """用例执行"""
        # string = '''<a href="/public/userprofile/%s/password/" role="button" class="btn btn-danger btn-xs active">快速重置密码</a> ''' % self.instance.id
        string = '''<a href="#" role="button" class="btn btn-danger btn-sm" onclick="password_rest(%d)">快速重置密码</a> ''' % self.instance.id
        if self.instance.id == 1:
            string = '''<a href="#" role="button" class="btn btn-danger btn-sm" onclick="password_rest(%d)">快速重置密码</a> ''' % self.instance.id
        return string

    reset.display_name = "操作密码"


class RoleAdmin(BaseAdmin):
    list_display = ("id", "rolename", "statue", "create_time", "update_time",)
    color_fields = {
        "statue": {
            "作废": "default",
            "有效": "success",
        }
    }
    # filter_horizontal = ["menus", ]


# 一层菜单名
class FirstLayerMenuAdmin(BaseAdmin):
    list_display = ['id', 'type', 'name', 'url_type', 'url_name', 'order']  # 显示字段表头


# 二层菜单名
class SubMenuMenuAdmin(BaseAdmin):
    list_display = ['id', 'name', 'url_type', 'url_name', 'order']  # 显示字段表头


class GroupsAdmin(BaseAdmin):
    list_display = ['id', 'name', 'description', ]
    # filter_horizontal = ["permissions", ]


class BusinessFuncAdmin(BaseAdmin):
    list_display = ("id", "name", "expression", "parameter", "description", "return_type", "type", "statue",)
    search_fields = ("name", "expression",)
    color_fields = {
        "statue": {
            "作废": "default",
            "有效": "success",
        }
    }
    list_editable = ["name","expression"]
    readonly_fields = ("expression",)
    list_filter = ("type", "statue",)
    ordering = "-expression"


class RetrievalAdmin(BaseAdmin):
    list_display = ("id", "name", "link", "statue",)
    search_fields = ("name", "link",)
    color_fields = {
        "statue": {
            "作废": "default",
            "有效": "success",
        }
    }

    list_filter = ("statue",)
    ordering = "-name"


class ResourceAdmin(BaseAdmin):
    list_display = ("id", "name", "link", "type", "color", "parent_menus","upload",)
    search_fields = ("name", "link",)
    list_filter = ("color", "type",)
    list_per_page = 15
    ordering = "-id"
    color_fields = {
        "color": {
            "default": "default",
            "success": "success",
            "info": "info",
            "warning": "warning",
            "primary": "primary",
            "danger": "danger",
        }
    }


class EnvironmentAdmin(BaseAdmin):
    list_display = ("id", "envir_id", "name",)


class DbinfoAdmin(BaseAdmin):
    list_display = ("id", "name", "dbtype", "dbhost", "dbport", "dbname", "dbuser", "dbpassword",)
    search_fields = ("name", "dbhost",)
    list_filter = ("dbtype",)


class LogServerinfoAdmin(BaseAdmin):
    list_display = ("id", "name", "logserver", "logport", "logname", "logpwd",)
    search_fields = ("name", "logserver",)


class ConfigurationsAdmin(BaseAdmin):
    list_display = ("id", "environment", "dbinfo", "log_server_info", "loglevel", "browserType", "is_task",
                    "task", "is_HiddenWindowBeforeStart", "is_CloseBrowserBeforeStart", "is_CloseBrowserAfterEnd",
                    "is_APIcaseFileCreate",
                    "is_APIcaseFileRemove", "is_ClearReportLogBeforeStart","test_integert", "update_time",)
    process_bar = ["test_integert",]
    list_editable = ["task",]
class CN_EN_MAPAdmin(BaseAdmin):
    list_display = ("id", "parent", "cn_name", "children", "statue", "create_time", "update_time",)
    list_per_page = 10
    search_fields = ("parent", "cn_name",)
    readonly_table = False  #设置为True后该表仅供读取
    color_fields = {
        "statue": {
            "作废": "default",
            "有效": "success",
        }
    }



class StepLogAdmin(BaseAdmin):
    list_display = ("id", "user", "action", "model_name","origin", "detail", "create_time", )
    list_per_page = 30
    list_filter = ("create_time",)
    search_fields =  ("user","model_name",)
    readonly_table = True  #设置为True后该表仅供读取
    wrap_flag =True

class TodoAdmin(BaseAdmin):
    list_display = ("user","content","statue","create_time",)
    list_filter = ("user","statue","create_time",)
    search_fields =  ("content",)
    wrap_flag = True


site.register(UserProfile, UserProfileAdmin)
site.register(Groups, GroupsAdmin)
site.register(Role, RoleAdmin)
site.register(FirstLayerMenu, FirstLayerMenuAdmin)
site.register(SubMenu, SubMenuMenuAdmin)
site.register(BusinessFunc, BusinessFuncAdmin)
site.register(Retrieval, RetrievalAdmin)
site.register(Resource, ResourceAdmin)
site.register(Environment, EnvironmentAdmin)
site.register(Dbinfo, DbinfoAdmin)
site.register(LogServerinfo, LogServerinfoAdmin)
site.register(Configurations, ConfigurationsAdmin)
site.register(CN_EN_MAP, CN_EN_MAPAdmin)
site.register(StepLog, StepLogAdmin)
site.register(TodoList, TodoAdmin)
