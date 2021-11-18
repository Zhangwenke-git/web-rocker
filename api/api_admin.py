from django.shortcuts import render, redirect
from core.base_admin import site, BaseAdmin
from django.forms import ValidationError
from django.http import JsonResponse
from api.models import *
from utils.pubulic.logger import Logger

logger = Logger("api_admin")


class ApiProjectAdmin(BaseAdmin):
    list_display = ("id", "name", "process", "last_execute", "execute", "expand","description", "statue","start","end",)
    list_per_page = 15
    search_fields = ("name",)
    list_filter = ("statue",)
    color_fields = {
        "statue": {
            "作废": "dark",
            "有效": "success",
        }
    }
    process_bar = ("process", "last_execute",)
    list_editable = ["name",]
    readonly_fields = ("last_execute",)
    def execute(self):
        """用例执行"""
        link_name = "执行"
        if self.instance.statue == 1:
            string = '''<a href="/api/apiproject/%d/execute/" role="button" class="button medium red">%s</a> ''' % (
                self.instance.id, link_name)
        else:
            string = '''<button  disabled="disabled" role="button" class="button medium red">%s</button> ''' % (link_name)
        return string

    execute.display_name = "执行"

    expand_flag = True

    def expand(self):
        string = """
        <a data-bs-toggle="collapse" data-bs-target="#collapseExample{id}" href="#collapseExample{id}" aria-expanded="false" aria-controls="collapseExample{id}">
        <span class="button medium white">查看关联</span>
        </a>

        """.format (id=self.instance.id)
        return string

    expand.display_name = "收展"


class TestSuitAdmin(BaseAdmin):
    list_display = ("id", "module", "class_title", "statue", "update_time", "execute", "expand",)
    list_per_page = 10
    search_fields = ("module", "class_title",)
    list_filter = ("statue",)
    #filter_horizontal = ("project",)
    actions = ['model_actions', ]  # 定制功能,测试返回到一个新页面
    # process_bar = ["class_title"]
    color_fields = {
        "statue": {
            "作废": "dark",
            "有效": "success",
        }
    }
    #list_editable = ["statue",]
    def execute(self):
        """用例执行"""
        link_name = "执行◀"
        if self.instance.statue == 1:

            string = '''<a href="/api/testsuit/%d/execute/" role="button" class="button medium red">%s</a> ''' % (
                self.instance.id, link_name)
        else:
            string = '''<button  disabled="disabled" role="button" class="button medium red">%s</button> ''' % (link_name)

        return string

    execute.display_name = "执行用例"

    expand_flag = True

    def expand(self):
        string = """
        <a data-bs-toggle="collapse" data-bs-target="#collapseExample{id}" href="#collapseExample{id}" aria-expanded="false" aria-controls="collapseExample{id}">
        <span class="button medium white">查看关联</span>
        </a>
        """.format (id=self.instance.id)
        return string

    expand.display_name = "收展"

    def model_actions(self, request, queryset):  # 对应的函数 #request类自己的请求  #arg2类的内容

        app_name = self.model._meta.app_label  # app名
        model_name = self.model._meta.model_name  # 表名
        objs = queryset  # 类对象
        action = request._admin_action
        logger.info(f"Prepare to execute operation: [{action}]")
        # if request.POST.get('delete_confirm') == 'yes':  # {#table_delete.html#}
        #     queryset.delete()
        #     return redirect('/%s/%s/' % (app_name, model_name))
        selected_ids = ','.join([str(i.id) for i in queryset])
        logger.debug(f'The selected ids are: [{selected_ids}]')
        return render(request, "api/testsuits_display.html", locals())

    model_actions.short_description = "生成测试用例XML"


class TestCaseAdmin(BaseAdmin):
    list_display = (
        "id", "case", "case_title", "templates", "test_suit", "statue",
        "execute", "case_description", "expand","update_time",)
    list_filter = ("test_suit", "templates",)  # 仅支持外键和枚举值
    search_fields = ("case", "case_title",)  # 必须加逗号
    #readonly_fields = ('case', 'case_title',)
    ordering = "-case"
    color_fields = {
        "statue": {
            "作废": "dark",
            "有效": "success",
        }
    }
    expand_flag = True

    def execute(self):
        """用例执行"""
        link_name = "执行◀"
        if self.instance.statue == 1:

            string = '''<a href="/api/testcase/%d/execute/" role="button" class="button medium red">%s</a> ''' % (
                self.instance.id, link_name)
        else:
            string = '''<button  disabled="disabled" role="button" class="button medium red">%s</button> ''' % (link_name)

        return string

    execute.display_name = "执行用例"

    def expand(self):
        string = """
        <a data-bs-toggle="collapse" data-bs-target="#collapseExample{id}" href="#collapseExample{id}" aria-expanded="false" aria-controls="collapseExample{id}">
        <span class="button medium white">查看关联</span>
        </a>

        """.format (id=self.instance.id)
        return string

    expand.display_name = "收展"


class TemplatesAdmin(BaseAdmin):
    list_display = ("id", "name", "statue", "method", "url", "table_name","check_template",)
    list_per_page = 10
    list_filter = ("method", "statue",)
    search_fields = ("name", "url",)
    right_flag = True
    color_fields = {
        "statue": {
            "作废": "dark",
            "有效": "success",
        }
    }

    def check_template(self):
        """查看模板"""
        string = '''<a href="/api/templates/%s/check/"  class="button medium white">查看模板</a> ''' % self.instance.id
        return string

    check_template.display_name = "表格查看"

    def default_form_validation(self, obj):
        tempate_name = obj.cleaned_data.get('name')  # 自制验证字段
        if len(tempate_name) < 3:
            return ValidationError(  # 添加错误信息 返回
                ("该字段%(field)s咨询内容记录不能少于3个字符"),
                code='invalid',
                params={'field': 'name', },
            )


class ScenarioAdmin(BaseAdmin):
    import_setting=True
    list_display = (
        "id", "scenario", "check", "priority", "test_case", "statue", "update_time",)
    list_per_page = 10
    list_filter = ("test_case", "priority", "statue",)
    search_fields = ("scenario",)
    list_editable = ["scenario",]
    color_fields = {
        "statue": {
            "作废": "dark",
            "有效": "success",
        },
        "priority": {
            "High": "gradient-bloody",
            "Medium": "gradient-blooker",
            "Low": "gradient-quepal",
        }

    }

    defined_add_link = "/api/scenarios/add/"
    check_flag = True

    def check(self):
        string = """
        <a class="button medium white" data-bs-toggle="collapse" data-bs-target="#collapseCheck{id}" href="#collapseCheck{id}" aria-expanded="false" aria-controls="collapseCheck{id}">表格查看</a>
        """ .format(id=self.instance.id)
        return string

    check.display_name = "表格查看"


class SqlAdmin(BaseAdmin):
    list_display = (
        "id", "name", "sql", "is_all", "field_list", "statue",  "update_time",)
    list_per_page = 10
    #filter_horizontal = ("case",)
    list_filter = ("is_all", "statue",)
    color_fields = {
        "statue": {
            "作废": "dark",
            "有效": "success",
        }}

class ExecutionRecordAdmin(BaseAdmin):
    list_display = (
        "id",  "create_date","module","project","case", "scenario", "result","start","path","create_time", "code",)
    list_per_page = 50
    readonly_table = True
    search_fields = ("project","module",)
    list_filter = ("create_date",)
    color_fields = {
        "result": {
            "Passed": "success",
            "Failed": "danger",
            "Error": "warning",
            "Skipped": "dark",
        }

    }


site.register(ApiProject, ApiProjectAdmin)
site.register(Templates, TemplatesAdmin)
site.register(TestSuit, TestSuitAdmin)
site.register(TestCase, TestCaseAdmin)
site.register(Scenario, ScenarioAdmin)
site.register(Sql, SqlAdmin)
site.register(ExecutionRecord, ExecutionRecordAdmin)
