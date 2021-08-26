from django import forms
from api import models
from django.forms import widgets
def CreateModelForm(request, admin_obj):
    class Meta:  # 调用内置方法
        model = admin_obj.model  # 获取表名
        fields = "__all__"  # 字段
        # type()就是一个最实用又简单的查看数据类型的方法。type()是一个内建的函数，调用它就能够得到一个反回值，从而知道想要查询的对像类型信息。

        exclude = admin_obj.modelform_exclude_fields

    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            column_obj = cls.Meta.model._meta.get_field(field_name)
            field_obj.widget.attrs['class'] = 'form-control form-control-sm mt-1 mb-3 ml-2'  # 前端的样式
            field_obj.widget.attrs['autocomplete'] = 'off'  # 前端的样式


            if field_obj.label.endswith("周期"):
                field_obj.widget.attrs.update({"data-type": "date-range", "class": "input-daterange-datepicker form-control"})

            if column_obj.get_internal_type() == "ManyToManyField":
                field_obj.widget.attrs.update({"class":"form-control form-control-sm mt-2"})

            if column_obj.get_internal_type() == "BooleanField":
                field_obj.widget.attrs.update({"class":"form-check-input ml-4 mb-2 mt-2"})

            # if column_obj.get_internal_type() == "TimeField":
            #     field_obj.widget.attrs.update({"data-type":"time","class":"form-control result"})
            #
            # if column_obj.get_internal_type() == "DateTimeField":
            #        field_obj.widget.attrs.update({"data-type":"datetime","class":"form-control result"})
            #
            # if column_obj.get_internal_type() == "DateField":
            #        field_obj.widget.attrs.update({"data-type":"datefield","class":"form-control result"})

            if column_obj.get_internal_type() == "TimeField":
                field_obj.widget.attrs.update({"class":"form-control form-control-sm"})
                field_obj.widget.input_type = "time"

            if column_obj.get_internal_type() == "DateTimeField":
                   field_obj.widget.input_type="datetime-local"
                   field_obj.widget.attrs.update({"class":"form-control form-control-sm"})

            if column_obj.get_internal_type() == "DateField":
                   field_obj.widget.input_type="date"
                   field_obj.widget.attrs.update({"class":"form-control form-control-sm"})


            if column_obj.get_internal_type() == "IntegerField":
                field_obj.widget.attrs.update({"class":"form-range","min":"0","max":"100"})
                field_obj.widget.input_type = "range"


            try:
                if field_obj.widget.input_type =="select" and not field_obj.widget.allow_multiple_selected:
                    field_obj.widget.attrs['class'] = 'single-select mt-1 mb-3'
                    #field_obj.widget.attrs['class'] = 'form-select form-select-sm mt-1 mb-3'
                if field_obj.widget.allow_multiple_selected:
                    field_obj.widget.attrs.update({"class":"multiple-select"})
            except Exception:
                pass

            if not hasattr(admin_obj, "is_add_form"):
                if field_name in admin_obj.readonly_fields:
                    field_obj.widget.attrs['disabled'] = True

        return forms.ModelForm.__new__(cls)

    def default_clean(self):
        from django.forms import ValidationError
        error_list = []
        from django.utils.translation import ugettext as _  # 国际化

        if admin_obj.readonly_table:  # 在这后端验证，防止黑客添加
            raise ValidationError(  # 添加错误信息
            _("该表单不可修改!"),
            code = 'invalid',)

        if self.instance.id:  # 表示为修改表单
            for field in admin_obj.readonly_fields:  # 如果是不可修改的字段
                field_val_from_db = getattr(self.instance, field)  # 取数据库中的值
                field_val = self.cleaned_data.get(field)  # 前端传来的值
                # ————————31PerfectCRM实现King_admin编辑多对多限制————————
                if hasattr(field_val_from_db, 'select_related'):  # 多对多
                    m2m_objs = getattr(field_val_from_db, 'select_related')().select_related()  # 调用多对多,获取对应的值
                    m2m_vals = [i[0] for i in m2m_objs.values_list('id')]  # 转为列表
                    set_m2m_vals = set(m2m_vals)  # 转集合  交集 数据库
                    set_m2m_vals_from_frontend = set([i.id for i in self.cleaned_data.get(field)])  # 前端的值  交集

                    if set_m2m_vals != set_m2m_vals_from_frontend:
                        error_list.append(ValidationError(
                            _("%(field)s: 该字段不可修改!"),
                            code='invalid',
                            params={'field': field, }))
                        self.add_error(field, "不可修改!")
                    continue

                if field_val_from_db != field_val:
                    error_list.append(ValidationError(
                        _("该字段%(field)s 不可修改,原值为: %(val)s"),
                        code='invalid',
                        params={'field': field, 'val': field_val_from_db}
                    ))

            for field in self.cleaned_data:  # 单独字段
                    if hasattr(admin_obj, 'clean_%s' % field):  # 是否有该字段的单独验证
                        field_clean_func = getattr(admin_obj, 'clean_%s' % field)  # 获取对应的函数
                        response = field_clean_func(self)
                        if response:
                            error_list.append(response)
                        if error_list:
                            raise ValidationError(error_list)

        response = admin_obj.default_form_validation(self)  # 可自定制
        if response:
            error_list.append(response)
        if error_list:
            raise ValidationError(error_list)

    dynamic_model_form = type("DynamicModelForm", (forms.ModelForm,), {"Meta": Meta})  # 生成modelform的类,
    setattr(dynamic_model_form, "__new__", __new__)
    setattr(dynamic_model_form, "clean", default_clean)
    return dynamic_model_form



