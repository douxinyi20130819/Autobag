from django.template import Library
from django.utils.safestring import mark_safe
from bag import models
import datetime ,time
register = Library()
def set_table(id):
    if int(id) == 1:
        table = models.UserProfile
    elif int(id) == 2:
        table = models.ReservationInfo
    else:
        table = models.Box
    return table

@register.simple_tag
def build_table_row(obj,title_list,id):
    ele = ""
    table = set_table(id)
    if title_list:
        for index, column_name in enumerate(title_list):
            # print('-----',index,column_name)
            column_obj = table._meta.get_field(column_name)
            if column_obj.choices:  # get_xxx_display
                column_data = getattr(obj, 'get_%s_display' % column_name)()
            else:
                column_data = getattr(obj, column_name)

            td_ele = "<td>%s</td>" % column_data
            if index == 0:
                td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id, column_data)

            ele += td_ele
    else:
        td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id, obj)

        ele += td_ele

    return mark_safe(ele)


@register.simple_tag
def get_model_verbose_name(id):
    table = set_table(id)
    return table._meta.verbose_name


