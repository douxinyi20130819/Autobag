from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_protect
from bag import models
from bag.admin import UserProfileAdmin
import json

from bag import form_handle

# Create your views here.
@login_required
def teacher_list(request):
    dict = {'teacher':'teacher','admin_info':'admin_info','id1':1,'id2':2,'id3':3}

    return render(request,"teacher_list.html",locals())

@login_required
def admin_info(request, teacher, admin_info, id):
    title, title_list, name, querysets = set_admin(id)
    if request.method == "POST":
        txt = request.POST.get("type",None)
        val = request.POST.get('data_id',None)
        if txt == "审核通过":
            obj = models.ReservationInfo.objects.filter(id=val)
            obj.update(status=1)
        elif txt == "拒绝":
            obj = models.ReservationInfo.objects.filter(id=val)
            obj.update(status=3)
        else:
            val_list = json.loads(val)

            for i in val_list:
                if i != "on":
                    obj = models.ReservationInfo.objects.filter(id=i).values("number__status")
                    if obj[0]["number__status"] == 1:
                        obj = models.ReservationInfo.objects.filter(id=i)
                        obj.update(status=3)
                    else:
                        obj = models.ReservationInfo.objects.filter(id=i)
                        obj.update(status=1)

    return render(request,"admin_info.html",locals())

@login_required
def admin_info_change(request, teacher, admin_info, admin_info_id,admin_info_change_id):

    model,fields,s,obj = get_admin_info_change(admin_info_id,admin_info_change_id)
    model_form = form_handle.create_dynamic_model_form(model,fields)

    if request.method == "GET":
        form_obj = model_form(instance=obj)
    elif request.method == "POST":
        form_obj = model_form(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/teacher/admin_info/%s/"%admin_info_id)

    return render(request, "admin_info_change.html",locals())


@login_required
def index(request):

    return render(request,"index.html")

def acc_login(request):
    error_msg = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            print("passed authencation", user)
            login(request, user)
            # request.user = user

            return redirect(request.GET.get('next', '/index/'))
        else:
            error_msg = "Wrong username or password!"
    return render(request, 'login.html', {'error_msg': error_msg})


def acc_logout(request):
    logout(request)
    return redirect("/login/")

@csrf_protect
def acc_register(request):
    if request.method == "GET":
        form_obj = UserProfileAdmin.add_form()
    elif request.method == "POST":
        form_obj = UserProfileAdmin.add_form(request.POST)
        if form_obj.is_valid():

            form_obj.save()
            return redirect("/login/")
        else:
            error_msg = "Wrong username or password!"

    return render(request,"register.html",locals())

@login_required
def acc_usesrinfo(request,user_id):
    # print(user_id)
    model = models.UserProfile
    fields = ['email', 'name', 'sex', 'old', 'grade', 'head_img', ]

    model_form = form_handle.create_dynamic_model_form(model,fields)
    obj = models.UserProfile.objects.get(id=user_id)
    if request.method == "GET":
        form_obj = model_form(instance=obj)
    elif request.method == "POST":
        form_obj = model_form(instance=obj,data=request.POST,files=request.FILES)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/index/")

    return render(request,"userinfo.html",locals())

def set_admin(id):
    if int(id) == 1:
        title = ['姓名', '性别', '年龄', '班级', '注册日期']
        title_list = ['name', 'sex', 'old', 'grade', 'date']
        name = '学生信息管理'
        querysets = models.UserProfile.objects.filter(is_superuser=False).order_by("-id")

    elif int(id) == 2:
        title = ['姓名', '柜号', '箱号', '状态', '开始日期','结束日期']
        title_list = ['name','Box','number', 'status', 'startdate', 'enddate']
        name = '预约信息管理'
        querysets = models.ReservationInfo.objects.all().order_by()

    else:
        title = ['箱柜号', '使用时间']
        title_list = ['box_name', 'use_date']
        name = '柜箱信息管理'
        querysets = models.Box.objects.all()
    return title,title_list,name,querysets

def get_admin_info_change(admin_info_id,admin_info_change_id):
    if int(admin_info_id) == 1:
        model = models.UserProfile
        obj = model.objects.get(id=admin_info_change_id)
        fields = ['name', 'sex', 'old', 'grade', 'role']
        img = model.objects.filter(id=admin_info_change_id)
        for s in img:
            pass
    elif int(admin_info_id) == 2:
        model = models.ReservationInfo
        obj = model.objects.get(id=admin_info_change_id)
        fields = ['name', 'Box', 'number', 'status', 'startdate', 'enddate']
        s = None

    else:
        model = models.Box
        obj = model.objects.get(id=admin_info_change_id)
        fields = ['box_name', 'use_date']
        s = None

    return  model,fields,s,obj