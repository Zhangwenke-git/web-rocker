# form.py
# ————————PerfectCRM实现king_admin行内编辑————————
from django import forms
from django.forms import ModelForm


def __new__(cls, *args, **kwargs):
    # super(CustomerForm, self).__new__(*args, **kwargs)
    # self.fields['customer_note'].widget.attrs['class'] = 'form-control'
    # disabled_fields = ['qq', 'consultant']
    for field_name in cls.base_fields:
        field = cls.base_fields[field_name]
        # print("field repr",field_name,field.__repr__())
        attr_dic = {'placeholder': field.help_text}  # 占位符: 帮助文本
        if 'BooleanField' not in field.__repr__():  # 布尔字段 不在 #__repr__()返回一个对象的 string 格式
            attr_dic.update({'class': 'form-control'})  # 更新
            # print("-->field",field)
            if 'ModelChoiceField' in field.__repr__():  # 模型选择字段 在 #__repr__()返回一个对象的 string 格式
                attr_dic.update({'data-tag': field_name})  # 更新  #数据标签
            # if 'DateTimeField' in field.__repr__():
            #     attr_dic.update({'placeholder': field_name})
        if cls.Meta.form_create is False:  # 表单创建   #是假
            if field_name in cls.Meta.admin.readonly_fields:  # 只读的字段
                attr_dic['disabled'] = True  # 禁用
                # print('----read only:',field_name)
        field.widget.attrs.update(attr_dic)  # 更新
        # for validators
        if hasattr(cls.Meta.model, "clean_%s" % field_name):  # hasattr() 函数用于判断对象是否包含对应的属性。
            clean_field_func = getattr(cls.Meta.model, "clean_%s" % field_name)  # getattr() 函数用于返回一个对象属性值。
            setattr(cls, "clean_%s" % field_name, clean_field_func)  # setattr 函数对应函数 getatt()，用于设置属性值，该属性必须存在。

        else:
            if hasattr(cls.Meta.model, "clean"):  # clean is kingadmin's own clean method
                clean_func = getattr(cls.Meta.model, "clean")  # getattr() 函数用于返回一个对象属性值。
                setattr(cls, "clean", clean_func)  # setattr 函数对应函数 getatt()，用于设置属性值，该属性必须存在。
            else:  # use default clean method
                setattr(cls, "clean", default_clean)  # setattr 函数对应函数 getatt()，用于设置属性值，该属性必须存在。
            return ModelForm.__new__(cls)


def default_clean(self):  # clear()方法用于清空(或删除)字典中的所有数据项。
    '''form defautl clean method'''
    # print("\[;mrun form defautl clean method...\[m",dir(self))
    # print(self.Meta.admin.readonly_fields)
    print("默认删除方法:", self.cleaned_data)
    # print("validataion errors:",self.errors)
    if self.Meta.admin.readonly_table is True:
        raise forms.ValidationError(("这是一个只读的表"))
    if self.errors:
        raise forms.ValidationError(("请补交之前修复错误。."))
    if self.instance.id is not None:  # 意味着这是一个改变形式,应该检查只读的字段
        for field in self.Meta.admin.readonly_fields:  # 循环 readonly_fields 不可修改字段
            old_field_val = getattr(self.instance, field)  # getattr() 函数用于返回一个对象属性值。
            form_val = self.cleaned_data.get(field)
            print("提出不同的比较:", old_field_val, form_val)
            if old_field_val != form_val:  # 如果旧字段和新字段不相等
                if self.Meta.partial_update:  # f可编辑的功能列表,只做部分检查
                    if field not in self.cleaned_data:  # 如果字段 不在  清理数据理
                        # 因为list_editable成生form时只生成了指定的几个字段，所以如果readonly_field里的字段不在，list_ediatble数据里，那也不检查了
                        continue  # continue 语句跳出本次循环

                self.add_error(field, "Readonly Field: field should be '{value}' ,not '{new_value}' ". \
                               format(**{'value': old_field_val, 'new_value': form_val}))


def create_form(model, fields, admin_obj, form_create=False, **kwargs):
    class Meta:
        pass

    setattr(Meta, 'model',model)  # 如果类自定义了__setattr__方法，当通过实例获取属性尝试赋值时，就会调用__setattr__。常规的对实例属性赋值，被赋值的属性和值会存入实例属性字典__dict__中。
    setattr(Meta, 'fields', fields)
    setattr(Meta, 'admin', admin_obj)
    setattr(Meta, 'form_create', form_create)  # 表单创建
    setattr(Meta, 'partial_update', kwargs.get("partial_update"))  # f可编辑的功能列表,只做部分检查

    attrs = {'Meta': Meta}
    name = 'DynamicModelForm'  # 动态模型的形式
    baseclasess = (ModelForm,)  # 模型形式
    model_form = type(name, baseclasess, attrs)  # type属性类型
    setattr(model_form, '__new__',__new__)  # 如果类自定义了__setattr__方法，当通过实例获取属性尝试赋值时，就会调用__setattr__。常规的对实例属性赋值，被赋值的属性和值会存入实例属性字典__dict__中。

    if kwargs.get("request"):  # 对表单验证器
        setattr(model_form, '_request', kwargs.get("request"))  # 将给定对象命名属性设置为指定的值。
    print(model_form)
    return model_form
# ————————PerfectCRM实现king_admin行内编辑————————

# form.py
