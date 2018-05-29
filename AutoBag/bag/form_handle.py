from django.forms import ModelForm
from bag import models


def create_dynamic_model_form(model_table, fields_list):
    """动态的生成modelform
    form_add: False 默认是修改的表单,True时为添加
    """

    class Meta:
        model = model_table
        # fields = ['name','consultant','status']
        fields = fields_list


    def __new__(cls, *args, **kwargs):
        # print("__new__",cls,args,kwargs)
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class':'form-control'})
        return  ModelForm.__new__(cls)

    dynamic_form = type("DynamicModelForm" ,(ModelForm,) ,{'Meta' :Meta,'__new__':__new__})
    # print(dynamic_form)
    return dynamic_form