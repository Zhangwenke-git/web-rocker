import json
from functools import reduce

from django import template
from django.core import serializers
from django.core.exceptions import FieldDoesNotExist
from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime, timedelta
import json2html

from backend.base_admin import site
from utils.pubulic.logger import Logger

logger = Logger("backend tag")
register = template.Library()

global false, null, true
false = False
true = True
null = ''


@register.simple_tag
def get_model_verbose_name(model_obj):
    """
    func:获取model的名称
    @param model_obj:
    @return:
    """
    model_name = model_obj._meta.verbose_name_plural if model_obj._meta.verbose_name else model_obj._meta.verbose_name_plural
    if not model_name:
        model_name = model_obj._meta.model_name
    return model_name


@register.simple_tag
def get_filed_list_cn_name(column_list, admin_obj):
    """
    func:获取model下要展示的字段中文名称verbose name
    @param column_list:
    @param admin_obj:
    @return:
    """
    cn_field_name = [admin_obj.model._meta.get_field(field).verbose_name for field in column_list]
    return cn_field_name


@register.simple_tag
def get_filed_cn_name(column, admin_obj):
    """
    func:获取字段对应的中文别名
    @param column:
    @param admin_obj:
    @return:
    """
    cn_field_name = "未注册中文名称"
    try:
        field_obj = admin_obj.model._meta.get_field(column)
        if type(field_obj).__name__ in ['ManyToManyField']:
            if hasattr(admin_obj, column):
                cn_field_name = getattr(admin_obj, column).display_name
                logger.debug(f"The verbose name of this many to many field is: {cn_field_name}")
        else:
            cn_field_name = field_obj.verbose_name
    except FieldDoesNotExist:
        if column == "id":
            cn_field_name = "序号"
        else:
            cn_field_name = getattr(admin_obj, column).display_name
    return cn_field_name


@register.simple_tag
def get_model_name(model_obj):
    """
    func:获取model的英文名称
    @param model_obj:
    @return:
    """
    model_name = model_obj._meta.model_name
    return model_name


@register.simple_tag
def get_app_name(model_obj):
    """
    func:获取app的名称， python manage.py startapp APPname
    @param model_obj:
    @return:
    """
    return model_obj._meta.app_label


@register.simple_tag
def build_table_row(admin_obj, obj):
    """
    func:获取任意一个表格数据
    @param admin_obj: 类似UserAdmin
    @param obj:<class 'public.models.Groups'>
    @return:
    """
    row_ele = ""
    column_not = []
    if admin_obj.list_display:
        for index, column in enumerate(admin_obj.list_display):

            try:
                column_obj = obj._meta.get_field(column)
                if column_obj.choices:  # 判断column_obj是否为外键
                    get_column_data = getattr(obj, "get_%s_display" % column)
                    column_data = get_column_data()
                    if column_data == "男":
                        column_data = "<img src='/static/picture/display/男性.svg' width='11'>"
                    elif column_data == "女":
                        column_data = "<img src='/static/picture/display/女性.svg' width='13'>"


                elif type(column_obj).__name__ in ['ManyToManyField']:  # 判断column_obj是否为多对多关系
                    if hasattr(admin_obj, column):
                        get_column_data = getattr(admin_obj, column)(obj)
                        column_data = get_column_data
                else:
                    column_data = getattr(obj, column)
                if type(column_data).__name__ == 'datetime':  # 判断column_obj是否为日期格式
                    column_data = column_data.strftime('%Y-%m-%d %H:%M:%S')

                if type(column_data).__name__ == 'ImageFieldFile':  # 判断column_obj是否为图片
                    if not column_data:
                        column_data = "static/picture/display/未知.svg"
                    column_data = """<img src="/%s" class="rounded-circle img-fluid" width="30" alt="">
                       """ % column_data

            except FieldDoesNotExist:
                logger.error(f"Fail to display the field :[{column}]")
                if hasattr(admin_obj, column):
                    column_func = getattr(admin_obj, column)
                    admin_obj.instance = obj
                    column_not.append(column)
                    admin_obj.column_not = column_not
                    column_data = column_func()

            if index == 0:
                hidden = "hidden" if admin_obj.readonly_table else ""
                td_ele = '''<td>
                <div class="d-flex order-actions">
                    <a class="text-danger" href="/{app_name}/{model_name}/{obj_id}/update/" {hidden}>
                        <i class="bx bxs-trash"></i>
                    </a>
                    
                    <a href="/{app_name}/{model_name}/{obj_id}/update/" class="text-primary ms-2" {hidden}>
                        <i class="bx bxs-edit"></i>
                    </a>
                    
                    <span class="text-secondary ms-1 mt-2"><strong>{column_data}</strong></span>
                </div>
                </td>'''.format(
                    app_name=admin_obj.model._meta.app_label, model_name=admin_obj.model._meta.model_name,
                    obj_id=obj.id, column_data=column_data, hidden=hidden)
            else:
                td_ele = "<td>%s</td>" % column_data

                if column in admin_obj.color_fields:  # 特定字段需要显示颜色
                    color_dic = admin_obj.color_fields[column]
                    if column_data in color_dic:
                        td_ele = "<td><span class='badge rounded-pill bg-%s'>%s</span></td>" % (
                            color_dic[column_data], column_data)

                if column in admin_obj.list_editable:  # 如果获取到king_admin配置list_editable的内容
                    td_ele = "<td>%s</td>" % render_list_editable_column(admin_obj, obj, column_obj)  # 到函数处理返回

                if column in admin_obj.process_bar:
                    if float(column_data) < 100:
                        td_ele = '''
                            <td><div class="progress" style="background: rgba(127, 99, 244, .1);width:150px;height:7px;">
                                <div class="progress-bar bg-primary" style="width: %s;" role="progressbar">
                            </div></div><span>%s</span></td>''' % (
                            str(column_data) + "%", str(column_data) + "%")
                    elif float(column_data) == 0:
                        td_ele = '''
                            <td><div class="progress" style="background: rgba(127, 99, 244, .1);width:150px;height:7px;">
                                <div class="progress-bar bg-danger" style="width: %s;" role="progressbar">
                                </div>
                            </div><span>%s</span></td>''' % (str(column_data) + "%", str(column_data) + "%")
                    else:
                        td_ele = '''
                            <td><div class="progress" style="background: rgba(127, 99, 244, .1);width:150px;height:7px;">
                                <div class="progress-bar bg-success" style="width: %s;" role="progressbar" >
                                </div>
                            </div><span>%s</span></td>''' % (str(column_data) + "%", str(column_data) + "%")

                if isinstance(column_data, bool):
                    bool_icon = """<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><polyline points="9 11 12 14 22 4"></polyline><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>	
                        """ if column_data else """<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>"""
                    bool_color = "style='color:green;'" if column_data else "style='color:red;'"
                    td_ele = "<td %s>%s</td>" % (bool_color, bool_icon)

            row_ele += td_ele
    else:
        row_ele += "<td>%s</td>" % obj
    return mark_safe(row_ele)


@register.simple_tag
def pag_omit(request, admin_obj):
    """
    func：对表格数据进行分页
    @param request:
    @param admin_obj:
    @return:
    """
    rest = ''
    add_tags = False
    order_by_url = generate_order_by_url(request)
    filters = generate_filter_url(admin_obj)
    for pages in admin_obj.querysets.paginator.page_range:
        if pages < 3 or pages > admin_obj.querysets.paginator.num_pages - 2 or abs(
                admin_obj.querysets.number - pages) <= 2:
            add_tags = False
            ele_class = ''
            if pages == admin_obj.querysets.number:  # 如果是当前页码,颜色加深 不进链接跳转
                ele_class = "active"
            rest += '''<li class="%s page-item"><a class="page-link" href="?page=%s%s%s">%s<span class="visually-hidden">(current)</span></a></li>''' \
                    % (ele_class, pages, order_by_url, filters, pages)
        else:
            if not add_tags:  # 如果不是标志位的页面
                rest += '<li><a>...</a></li>'
                add_tags = True

    return mark_safe(rest)


@register.simple_tag
def generate_filter_url(admin_obj):
    """
    func:拼接筛选的url
    @param admin_obj:
    @return: 含有筛选条件的Url
    """
    url = ''
    for k, v in admin_obj.filter_condtions.items():
        url += "&%s=%s" % (k, v)
    return url


@register.simple_tag
def get_orderby_key(request, column):
    """
    func:对表格的表头进行排序
    @param request:
    @param column: 字段值
    @return:
    """
    current_order_by_key = request.GET.get("_o")
    search_key = request.GET.get("_q")

    if search_key != None:
        if current_order_by_key != None:  # 如果不为空，肯定有某列被排序了
            if current_order_by_key == column:  # 判断是否相等，则当前这列正在被排序
                if column.startswith("-"):  # startsWith是String类中的一个方法，用来检测某字符串是否以另一个字符串开始，返回值为boolean类型
                    return column.strip("-")  # strip去掉
                else:
                    return "-%s&_q=%s" % (column, search_key)
        return "%s&_q=%s" % (column, search_key)
    else:
        if current_order_by_key != None:  # 如果不为空，#肯定有某列被排序了
            if current_order_by_key == column:  # 判断是否相等，则当前这列正在被排序
                if column.startswith("-"):  # startsWith是String类中的一个方法，用来检测某字符串是否以另一个字符串开始，返回值为boolean类型
                    return column.strip("-")  # strip去掉
                else:
                    return "-%s" % column
        return column


@register.simple_tag
def display_order_by_icon(request, column):
    """
    func:排序时显示ICON
    @param request:
    @param column:
    @return:
    """
    current_order_by_key = request.GET.get("_o")
    if current_order_by_key != None:  # 肯定有某列被排序了
        if current_order_by_key.strip("-") == column:
            if current_order_by_key.startswith("-"):
                dir = "lni lni-arrow-down"
            else:
                dir = "lni lni-arrow-up"
            ele = """<i style='color: gary;' class='%s'></i>""" % dir
            return mark_safe(ele)
    return ''


@register.simple_tag
def get_current_orderby_key(request):  # 注意生成的URL问题
    """
    func:过滤后的排序功能
    @param request:
    @return:
    """
    current_order_by_key = request.GET.get("_o")
    return current_order_by_key or ''


@register.simple_tag
def generate_order_by_url(request):
    """
    func:排序功能
    @param request:
    @return:
    """
    current_order_by_key = request.GET.get("_o")
    if current_order_by_key != None:  # 肯定有某列被排序了
        return "&_o=%s" % current_order_by_key
    return ''


@register.simple_tag
def get_search_key(request):
    """
    func:搜索框保留值
    @param request:
    @return:
    """
    search_key = request.GET.get("_q")
    return search_key or ''


@register.simple_tag
def get_filter_field(filter_column, admin_obj):
    """
    func:外键下拉筛选数据表
    @param filter_column:
    @param admin_obj:
    @return:
    """
    select_ele = """<select class="mr-sm-2 single-select" name='{filter_column}'><option  value="">---------</option>"""  # 拼接成下拉框返回
    field_obj = admin_obj.model._meta.get_field(filter_column)  # 调用内置方法
    selected = ''
    if field_obj.choices:
        for choice_item in field_obj.choices:
            if admin_obj.filter_condtions.get(filter_column) == str(choice_item[0]):
                selected = "selected"
            select_ele += """<option value="%s" %s>%s</option> """ % (choice_item[0], selected, choice_item[1])
            selected = ""

    if type(field_obj).__name__ in ['ForeignKey', 'ManyToManyField', 'OneToOneField']:  # 外健属性
        for choice_item in field_obj.get_choices()[1:]:
            if admin_obj.filter_condtions.get(filter_column) == str(choice_item[0]):  # 就是选择的这个条件，整数转字符串
                selected = "selected"
            select_ele += """<option value="%s" %s>%s</option> """ % (choice_item[0], selected, choice_item[1])
            selected = ''

    if type(field_obj).__name__ in ['DateTimeField', 'DateField']:  # 如果是时间格式
        date_els = []  # 日期条件项
        today_ele = datetime.now().date()  # 今天日期
        date_els.append(['今天', today_ele])  # 今天
        date_els.append(['昨天', today_ele - timedelta(days=1)])  # 昨天
        date_els.append(['近7天', today_ele - timedelta(days=7)])  # 一周
        date_els.append(['近30天', today_ele - timedelta(days=30)])  # 三十
        date_els.append(['本月', today_ele.replace(day=1)])  # 本月
        date_els.append(['近90天', today_ele - timedelta(days=90)])  # 90天
        date_els.append(['近365天', today_ele - timedelta(days=365)])  # 365天
        date_els.append(['本年', today_ele.replace(month=1, day=1)])  # 今年

        for choice_item in date_els:
            if admin_obj.filter_condtions.get("%s__gte" % filter_column) == str(choice_item[1]):
                selected = 'selected'
            select_ele += """<option value="%s" %s>%s</option> """ % (choice_item[1], selected, choice_item[0])
            selected = ''
        filter_column_name = "%s__gte" % filter_column
    else:
        filter_column_name = filter_column

    select_ele += "</select>"
    select_ele = select_ele.format(filter_column=filter_column_name)  # 格式化时间的判断条件
    return mark_safe(select_ele)


@register.simple_tag
def get_admin_actions(admin_obj):
    """
    func:获取批量操作
    @param admin_obj:
    @return:
    """
    options = "<option value='-1'>-------</option>"  # 默认为空
    actions = admin_obj.default_actions + admin_obj.actions  # 默认加自定制
    for action in actions:
        logger.debug(f"Prepare to execute: {action}!")
        action_func = getattr(admin_obj, action)  # 功能方法
        if hasattr(action_func, "short_description"):  # 反射如有自定义的名称执行函数方法
            action_name = action_func.short_description  # 等于自定义的名称 #显示中文
        else:
            action_name = action  # 等于函数名称
        options += """<option value="{action_func_name}">{action_name}</option> """.format(action_func_name=action,
                                                                                           action_name=action_name)
    return mark_safe(options)


# ————————59PerfectCRM实现king_admin行内编辑————————
def render_list_editable_column(admin_obj, obj, column_obj):  # 处理def build_table_row(admin_obj,obj,request):的行内编辑内容
    # print(table_obj,row_obj,field_obj,field_obj.name,field_obj.get_internal_type())
    data_type = ("PositiveSmallIntegerField", "SmallIntegerField", "CharField", "EmailField", "TextField", 'ForeignKey')
    # 'BooleanField','   # "IntegerField", 'BigIntegerField', "BinaryField",   "FileField", "ImageField", "NullBooleanField", "URLField"
    # 'DateField, "DecimalField"  , "TimeField", ,"AutoField" ,  ,"OneToOneField" "ManyToManyField"
    if column_obj.get_internal_type() in data_type:  # 检测数据库类型

        column_data = column_obj.value_from_object(obj)
        if not column_obj.choices and column_obj.get_internal_type() != "ForeignKey":  # 如果不是选择框类型和外健框类型
            column = '''<input data-tag='editable' class='form-control ' style='min-width:200px;' type='text' name='%s' value='%s' disabled required>''' % \
                     (column_obj.name,
                      column_obj.value_from_object(obj) or '')  # 返回这个字段的值在给定的模型实例


        else:
            # if field_obj.get_internal_type() == "ForeignKey":
            #     column = '''<select data-tag='editable' class='form-control'  name='%s' >'''%field_obj.name
            # else:
            column = '''<select data-tag='editable' class='single-select' style='min-width:200px;' required disabled name='%s' >''' % column_obj.name  # 如果是选择框类型和外健框类型
            for option in column_obj.get_choices():  # 返回选择一个默认的空白的选择包括,使用SelectField选择这个领域。
                if option[0] == column_data:
                    selected_attr = "selected"
                else:
                    selected_attr = ''
                column += '''<option value='%s' %s >%s</option>''' % (option[0], selected_attr, option[1])
            column += "</select>"
    elif column_obj.get_internal_type() == 'BooleanField':  # 如果是勾选类型
        column_data = column_obj.value_from_object(obj)
        if column_data == True:  # 如果前端返回的数据等于真
            checked = 'checked'  # 勾选框显示打勾
        else:
            checked = ''  # 勾选框显示空
        column = '''<input data-tag='editable' type='checkbox' name='%s' value="%s"  %s> ''' % (
            column_obj.name, column_data, checked)

    elif column_obj.get_internal_type() == "DateTimeField":
        column = '''<input data-tag='editable' class='form-control' type='datetime-local'  name='%s' value='%s' disabled required>''' % \
                 (column_obj.name,
                  column_obj.value_from_object(obj))  # 返回这个字段的值在给定的模型实例。
    elif column_obj.get_internal_type() == "DateField":
        column = '''<input data-tag='editable' class='form-control ' type='date'  name='%s' value='%s' disabled required>''' % \
                 (column_obj.name,
                  column_obj.value_from_object(obj))  # 返回这个字段的值在给定的模型实例。
    elif column_obj.get_internal_type() == "TimeField":
        column = '''<input data-tag='editable' class='form-control ' type='time'  name='%s' value='%s' disabled required>''' % \
                 (column_obj.name,
                  column_obj.value_from_object(obj))  # 返回这个字段的值在给定的模型实例。

    else:
        column = column_obj.value_from_object(obj)  ##返回这个字段的值在给定的模型实例。
    return column


# ————————59PerfectCRM实现king_admin行内编辑————————


@register.simple_tag
def display_all_related_obj(objs):
    """
    func:取出对象及所有相关联的数据
    @param objs:
    @return:
    """
    from django.db.models.query import QuerySet
    if type(objs) != QuerySet:
        objs = [objs, ]
    if objs:
        model_class = objs[0]._meta.model  # 取表对象
        model_name = objs[0]._meta.model_name  # 取表名
        return mark_safe(recursive_related_objs_lookup(objs))


def recursive_related_objs_lookup(objs, name=None, conn_batch_size=0):
    # objs  <QuerySet [<TestSuit: XBOND>]> <class 'django.db.models.query.QuerySet'>

    name = set()
    # 开始标签的拼接
    ul_ele = "<ul style='color: gray;font-weight:bold'>"

    for obj in objs:
        li_ele = '''<li>{0}:{1}</li>'''.format(obj._meta.verbose_name, obj.__str__().strip("<>"))
        ul_ele += li_ele

        for m2m_field in obj._meta.local_many_to_many:  # local_many_to_many返回列表，many_to_many返回元祖
            sub_ul_ele = "<ul style='color: red'>"
            m2m_field_obj = getattr(obj, m2m_field.name)  # 反射 如果有选项

            for m2m_data in m2m_field_obj.select_related():
                sub_li_ele = '''<li>{}:{}</li>'''.format(m2m_field.verbose_name, m2m_data.__str__().strip("<>"))
                sub_ul_ele += sub_li_ele
            sub_ul_ele += '</ul>'
            ul_ele += sub_ul_ele
        # <---------------------------外健关联处理------------------------------------
        for related_obj in obj._meta.related_objects:
            if hasattr(obj, related_obj.get_accessor_name()):
                accessor_obj = getattr(obj, related_obj.get_accessor_name())
                if hasattr(accessor_obj, 'select_related'):
                    target_object = accessor_obj.select_related()

                    if 'ManyToManyRel' in related_obj.__repr__():
                        sub_ul_ele = '<ul style="color: green">'
                        for data in target_object:
                            sub_li_ele = '''<li>{0}:{1}</li>'''.format(data._meta.verbose_name,
                                                                       data.__str__().strip("<>"))
                            sub_ul_ele += sub_li_ele
                        sub_ul_ele += '</ul>'
                        ul_ele += sub_ul_ele

                    # <---------------递归处理-------------------
                    if len(target_object) != conn_batch_size:
                        names = target_object.__str__()
                        if names == name:
                            ul_ele += '</ul>'
                            return ul_ele
                        else:
                            conn_batch_size = conn_batch_size + 1
                            node = recursive_related_objs_lookup(target_object, name=names,
                                                                 conn_batch_size=conn_batch_size)
                            ul_ele += node

                    # <---------------由于使用递归，下面的标签样会发生重复，就不需要使用了--------------------
                else:
                    target_object = accessor_obj
                    print("外健关联 一对一：", target_object, '属性：', type(target_object))
    ul_ele += '</ul>'
    return ul_ele


@register.simple_tag
def get_m2m_available_objs(admin_obj, field_name):
    '''
    func:获取待选的数据
    @param admin_obj:
    @param field_name:
    @return:
    '''
    # c= admin_obj.model.tags.rel.model.objects.all()
    # print('c',c)
    # m2m_objs= admin_obj.model.tags.rel.model.objects.all()
    # print('m2m_objs',m2m_objs)
    m2m_model = getattr(admin_obj.model, field_name).rel  # 复选框对象
    m2m_objs = m2m_model.model.objects.all()  # 获取到复选框所有内容
    return m2m_objs


@register.simple_tag
def get_m2m_chosen_objs(admin_obj, field_name, obj):
    """
    func:获取复选框中已选的数据
    @param admin_obj:
    @param field_name:
    @param obj:
    @return:
    """
    if obj.id:
        return getattr(obj, field_name).all()
    return []


def create_table_row(admin_obj, obj, flag):
    """
    func:获取任意一个表格数据
    @param admin_obj: 类似UserAdmin
    @param obj:<class 'public.models.Groups'>
    @return:
    """

    row_ele = ""
    if flag:
        row_ele = '<td><input tag="obj_checkbox" type="checkbox" value="%d"></td>' % obj.id
    if admin_obj.simple_list:
        for index, column in enumerate(admin_obj.simple_list):
            try:
                column_obj = obj._meta.get_field(column)
                if column_obj.choices:  # 判断column_obj是否为外键
                    get_column_data = getattr(obj, "get_%s_display" % column)
                    column_data = get_column_data()

                elif type(column_obj).__name__ in ['ManyToManyField']:  # 判断column_obj是否为多对多关系
                    if hasattr(admin_obj, column):
                        get_column_data = getattr(admin_obj, column)(obj)
                        column_data = get_column_data
                else:
                    column_data = getattr(obj, column)
                if type(column_data).__name__ == 'datetime':  # 判断column_obj是否为日期格式
                    column_data = column_data.strftime('%Y-%m-%d %H:%M:%S')


            except FieldDoesNotExist:
                logger.error(f"Fail to display the field :[{column}]")

            else:
                if column in admin_obj.color_fields:  # 特定字段需要显示颜色
                    color_dic = admin_obj.color_fields[column]
                    if column_data in color_dic:
                        td_ele = "<td><span class='badge rounded-pill bg-%s'>%s</span></td>" % (
                            color_dic[column_data], column_data)
                    else:
                        td_ele = "<td>%s</td>" % column_data
                else:
                    td_ele = '''<td>%s</td>''' % column_data
            row_ele += td_ele
    else:
        row_ele += "<td>%s</td>" % obj

    return mark_safe(row_ele)


@register.simple_tag
def display_all_related_data(objs, flag=False):
    """
    func:取出对象及所有相关联的数据
    @param objs:
    @return:
    """
    from django.db.models.query import QuerySet

    if type(objs) != QuerySet:
        objs = [objs, ]
    if objs:
        model_class = objs[0]._meta.model  # 取表对象
        model_name = objs[0]._meta.model_name  # 取表名
        data_string = recursive_related_data_lookup(objs, flag)
        return mark_safe(data_string)


def recursive_related_data_lookup(objs, flag):
    admin_obj = None

    for obj in objs:
        table_str_list = []
        simple_list = []

        for related_obj in obj._meta.related_objects:
            if hasattr(obj, related_obj.get_accessor_name()):
                accessor_obj = getattr(obj, related_obj.get_accessor_name())
                if hasattr(accessor_obj, 'select_related'):
                    target_object = accessor_obj.select_related()
                else:
                    target_object = accessor_obj
                result_list = []
                for object in target_object:
                    from backend.base_admin import site
                    app_name, model_name = object._meta.__str__().split(".")
                    admin_obj = site.registered_sites[app_name][model_name]
                    simple_list = []
                    for index, column in enumerate(admin_obj.list_display):
                        # if column not in ["update_time", "create_time", "expand", "execute"]:
                        if column not in ["create_time", "expand", "execute", "check", "check_template"]:
                            simple_list.append(column)
                    admin_obj.simple_list = simple_list
                    result = create_table_row(admin_obj, object, flag)
                    if flag:
                        tr_str = "<tr>" + result + "</tr>"
                        if "作废" not in tr_str:
                            result_list.append(tr_str)
                    else:
                        result_list.append("<tr style='background: rgba(127, 99, 244, .1)'>" + result + "</tr>")
                result = ''.join(result_list)
                result = "<tbody>" + result + "</tbody>"

                if result == "<tbody></tbody>":
                    result = '<tbody><tr><td><span style="color:gray;">There is no related data!</span></td></tr></tbody>'

                if len(simple_list) == 0:
                    result = '<span style="color:gray;">There is no related data!</span>'

                th = "<th><input type='checkbox' onclick='SelectAll(this);'></th>" if flag else ""

                for field in simple_list:
                    th_cn = get_filed_cn_name(field, admin_obj)
                    th_string = f"<th style='font-size:smaller;'>{th_cn}</th>"
                    th += th_string

                headline = f"<thead><tr style='background: rgba(127, 99, 244, .1)'>{th}</tr></thead>" if flag else f"<thead><tr>{th}</tr></thead>"
                result = "<table class='table table-responsive-sm text-wrap small'>" + headline + result + "</table>"
                table_str_list.append(result)
    sub_table_str = "".join(table_str_list)
    return sub_table_str


def dict_merge(dict1, dict2):
    return dict(dict1, **dict2)


@register.simple_tag
def display_as_table(objs):
    """
    func:取出对象及所有相关联的数据
    @param objs:
    @return:
    """
    from django.db.models.query import QuerySet

    if type(objs) != QuerySet:
        objs = [objs, ]
    if objs:
        objs = objs[0]
        merge_info = dict()

        merge_info["parameter"] = reduce(dict_merge, eval(objs.parameter))
        merge_info["validator"] = reduce(dict_merge, eval(objs.validator))
        table_html = json2html.json2html.convert(merge_info)
        table_html = table_html.replace('table border="1"',
                                        'table class="table table-bordered text-wrap"').replace(
            '<tr>', '<tr>'
        ).replace('<th>', '<th class="text-secondary">')

        return mark_safe(table_html)


@register.simple_tag
def display_as_formatted_table(objs):
    """
    func:取出对象及所有相关联的数据
    @param objs:
    @return:
    """
    from django.db.models.query import QuerySet

    if type(objs) != QuerySet:
        objs = [objs, ]
    if objs:
        objs = objs[0]
        parameter = reduce(dict_merge, eval(objs.parameter))
        case_template = objs.test_case.templates.data
        from jinja2 import Template
        template = Template(case_template)
        formatted_string = template.render(parameter)
        formatted_merge_info = eval(formatted_string)

        formatted_table_html = json2html.json2html.convert(formatted_merge_info)
        formatted_table_html = formatted_table_html.replace('table border="1"',
                                                            'table class="table table-bordered text-wrap"').replace(
            '<tr>', '<tr>'
        ).replace('<th>', '<th class="text-secondary">').replace('<td>${', '<td class="text-danger">${')

        for k, v in parameter.items():
            formatted_table_html = formatted_table_html.replace(f'<td>{v}', f'<td class="text-primary">{v}')

        return mark_safe(formatted_table_html)


@register.simple_tag
def load_icon(app, firstmenus):
    from public.models import Resource
    type_dict = {"api": 0, "web": 1, "public": 2}
    color_dict = {
        0: "default",
        1: "primary",
        2: "info",
        3: "success",
        4: "danger",
        5: "warning",
    }
    result = Resource.objects.filter(type=type_dict.get(app), parent_menus=firstmenus)
    html = ""
    for icon in result:
        if not icon.upload:
            path = "/static/picture/icon/default.svg"
        else:
            path = "/" + str(icon.upload)

        sub_html = f"""
       
		<div class="col">
            <div class="card radius-10">
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        <div>
                            <a href="{icon.link}"><h5 class="my-1 text-secondary">{icon.name}</h4></a>
                            <p class="mb-0 text-secondary">{icon.link}</p>
                        </div>
                        <div class="text-{color_dict.get(icon.color)} ms-auto font-35"><img src="{path}" alt="...">
                        </div>
                    </div>
                </div>
            </div>
       </div>

        """

        html = html + sub_html
    return mark_safe(html)


@register.simple_tag
def display_database():
    from public.models import Dbinfo
    db = Dbinfo.objects.all()
    html_str = ""
    for item in db:
        html_str += """<option value='%s'>%s-%s</option>""" % (item.name, item.name, item.dbhost)
    return mark_safe(html_str)


@register.simple_tag
def display_logserver():
    from public.models import LogServerinfo
    db = LogServerinfo.objects.all()
    html_str = ""
    for item in db:
        html_str += """<option value='%s'>%s-%s</option>""" % (item.name, item.name, item.logserver)
    return mark_safe(html_str)


@register.simple_tag
def show_step_log():
    from public.models import StepLog, UserProfile
    log_recoder = StepLog.objects.order_by("-id").values()[:20]

    li_elements = "暂无记录"
    li_element_list = []
    for recoder in log_recoder:
        user = recoder["user"]
        user_info = model_to_dict(UserProfile.objects.filter(username=user).first())
        avatar = user_info["photo"]
        photo = f'<img src="/{avatar}" class="msg-avatar" alt="user avatar">'
        if avatar == "":
            photo = '<img src="/static/picture/display/未知.svg" class="msg-avatar" alt="user avatar">'

        if recoder['action'] == "新增":
            color = "text-success"
        elif recoder['action'] == "删除":
            color = "text-danger"
        else:
            color = "text-warning"
        app_name, model_name = recoder['model_name'].split("-")
        admin_obj = site.registered_sites[app_name][model_name]
        tb_nm = admin_obj.model._meta.verbose_name_plural

        # detail = f"<span class='{color}'>{recoder['action']}</span>表<span class='text-info'>{tb_nm}</span>记录，<a href='javascript:void(0)' onclick='check_log_details({recoder['id']})'>查看详情</a>"
        detail = f"<span class='{color}'>{recoder['action']}</span>表<span class='text-info'>{tb_nm}</span>记录，<a href='javascript:void(0)' onclick='check_log_details({recoder['id']})'>查看详情</a>"
        log_time = recoder["create_time"].strftime('%Y-%m-%d %H:%M:%S')
        html_str = """

            <li class="dropdown-item">
                <div class="row col-lg-12">
                    <div class="col-lg-2">
                        %s
                    </div>
                    <div class="col-lg-10">
                        <h6 class="msg-name">%s<span class="msg-time float-end">%s</span></h6>
                        <p class="msg-info">%s</p>
                    </div>
                </div>
            </li>

        """ % (photo, user, log_time, detail)

        li_element_list.append(html_str)
        li_elements = "".join(li_element_list)
    return mark_safe(li_elements)
