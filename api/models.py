# -*-coding=utf-8-*-
import datetime

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class RollingPic(models.Model):
    pictureName = models.CharField(verbose_name="图片名称", max_length=32)
    path = models.FileField(upload_to='./static/crm/images/rollingPicture', verbose_name='图片路径')
    description = models.TextField(verbose_name='图片描述', max_length=320)

    class Meta:
        verbose_name_plural = '巨幕管理'


class ApiProject(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='项目名称')
    description = models.CharField(max_length=320, blank=True, null=True, verbose_name='项目描述')
    start = models.DateField(max_length=64,blank=True,null=True, verbose_name='项目开始')
    end = models.DateField(max_length=64,blank=True,null=True, verbose_name='项目结束')
    statue_choice = (
        (0, "作废"),
        (1, "有效"),
    )
    statue = models.SmallIntegerField(choices=statue_choice, default=1, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name_plural = 'API项目管理'

    def __str__(self):
        return self.name


class TestSuit(models.Model):
    module = models.CharField(max_length=64, unique=True, verbose_name='Py文件名称',help_text=mark_safe("""
        <span style="color:gray;font-size:smaller;" class="glyphicon glyphicon-question-sign">填写PY测试文件名称，为字符串形式，建议首字母大写，例如：Login </span>
    """))
    class_title = models.CharField(max_length=32, blank=True, null=True, verbose_name='测试类名称')
    project = models.ManyToManyField(ApiProject, verbose_name='所属项目',help_text=mark_safe('<p class="text-dark small mt-1">Tips:hold down <kbd><kbd>ctrl</kbd></kbd>, to select more than one.</p>'))
    statue_choice = (
        (0, "作废"),
        (1, "有效"),
    )
    statue = models.SmallIntegerField(choices=statue_choice, default=1, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name_plural = '用例集'

    def __str__(self):
        return self.module


class Templates(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='模板名称')
    url = models.URLField(max_length=128, verbose_name='URL地址')
    method_choice = (
        (0, "GET"),
        (1, "POST"),
        (3, "PUT"),
        (4, "DELETE"),
    )
    method = models.SmallIntegerField(choices=method_choice, default=1, verbose_name="请求方式")
    header = models.CharField(max_length=640, null=True, default="{'Content-Type':'application/json'}",
                              verbose_name='header')
    data = models.TextField(max_length=2400, verbose_name='请求模板', help_text=mark_safe("""
    
    <div class="alert border-0 border-start border-5 border-primary alert-dismissible fade show py-2">
        <div class="d-flex align-items-center">
            <div class="font-35 text-primary"><i class='bx bx-bookmark-heart'></i>
            </div>
            <div class="ms-3">
                <h6 class="mb-0 text-primary">提醒</h6>
                <div>
                ① 常规变量使用{{}}标识，例如：{{username}} <br>② 调用其他函数，则使用${function}|<>形式标识 <br>③ 需传参的函数，则使用${login}|<{{username}},{{password}}>标识 </span>
                </div>
            </div>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    
    """))

    process_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='进程名称')
    linux_order_str = models.CharField(max_length=100, blank=True, null=True, verbose_name='linux命令')
    table_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='所需表名')
    statue_choice = (
        (0, "作废"),
        (1, "有效"),
    )
    statue = models.SmallIntegerField(choices=statue_choice, default=1, verbose_name="状态")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name_plural = '请求接口模板'

    def __str__(self):
        return self.name


class TestCase(models.Model):
    case = models.CharField(max_length=64, unique=True, verbose_name='测试用例', help_text=mark_safe("""
        <span style="color:gray;font-size:smaller;" class="glyphicon glyphicon-question-sign">填写函数名称，建议全部小写，为字符串形式，例如：login_api </span>
    """))
    case_title = models.CharField(max_length=100, verbose_name='测试用例名称')
    case_description = models.CharField(max_length=320, blank=True, null=True, verbose_name='测试用例描述')
    templates = models.OneToOneField(Templates, verbose_name='模板', on_delete=models.CASCADE)
    test_suit = models.ForeignKey(TestSuit, verbose_name='用例集合', on_delete=models.CASCADE)
    statue_choice = (
        (0, "作废"),
        (1, "有效"),
    )
    statue = models.SmallIntegerField(choices=statue_choice, default=1, verbose_name="状态")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name_plural = '用例函数'

    def __str__(self):
        return "%s-%s" % (self.case_title,self.case)


class Scenario(models.Model):
    scenario = models.CharField(max_length=64, unique=True, verbose_name='场景名称',help_text=mark_safe("""
        <span style="color:gray;font-size:smaller;" class="glyphicon glyphicon-question-sign">填写测试场景名称，例如：用户名正确-密码错误 </span>
    """))
    parameter = models.TextField(max_length=2000, verbose_name='请求参数')
    validator = models.CharField(max_length=100, default=200,verbose_name='验证字段')

    priority_choice = (
        (0, "High"),
        (1, "Medium"),
        (2, "Low"),
    )
    priority = models.SmallIntegerField(choices=priority_choice, default=0, verbose_name="优先级")
    test_case = models.ForeignKey(TestCase, verbose_name='测试函数（用例）', on_delete=models.CASCADE)
    statue_choice = (
        (0, "作废"),
        (1, "有效"),
    )
    statue = models.SmallIntegerField(choices=statue_choice, default=1, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name_plural = '用例场景'

    def __str__(self):
        return self.scenario  # 不添加这个的话，多对多关系中会提示：XXX.onject1,XXX.onject2,




class Sql(models.Model):
    name = models.CharField(max_length=64,verbose_name='名称')
    sql = models.CharField(max_length=640,verbose_name='sql语句')

    is_all = models.BooleanField(default=1, verbose_name="是否全量输出")
    field_list = models.CharField(max_length=320,verbose_name='字段列表')

    case = models.ManyToManyField(TestCase, verbose_name='所涉用例',help_text=mark_safe('<p class="text-dark small mt-1">Tips:hold down <kbd><kbd>ctrl</kbd></kbd>, to select more than one.</p>'))
    statue_choice = (
        (0, "作废"),
        (1, "有效"),
    )
    statue = models.SmallIntegerField(choices=statue_choice, default=1, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

