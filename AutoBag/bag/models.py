
# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='账户',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=64,verbose_name="姓名")
    sex_choices = ((0, '男'), (1, '女'))
    sex = models.PositiveSmallIntegerField(choices=sex_choices, blank=True, null=True,verbose_name="性别")
    old = models.IntegerField(blank=True, null=True,verbose_name="年龄")
    grade = models.CharField(max_length=64, blank=True, null=True,verbose_name="班级")
    head_img = models.ImageField(upload_to='imgs',max_length=128,verbose_name="照片")

    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    role = models.ManyToManyField("Role", blank=True, null=True,default='')
    #is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.name


    class Meta:
        permissions = (
            # ('crm_table_list', '可以查看kingadmin每张表里所有的数据'),
            # ('crm_table_list_view', '可以访问kingadmin表里每条数据的修改页'),
            # ('crm_table_list_change', '可以对kingadmin表里的每条数据进行修改'),
            # ('crm_table_obj_add_view', '可以访问kingadmin每张表的数据增加页'),
            # ('crm_table_obj_add', '可以对kingadmin每张表进行数据添加'),
        )
        verbose_name = "用户表"

class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=64,unique=True,verbose_name="角色")
    menus = models.ManyToManyField("Menus",blank=True,verbose_name="菜单")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色表"


# class StudentInfo(models.Model):
#     """学生信息"""
#     name = models.CharField(max_length=64, default=None)
#     sex_choices = ((0, '男'), (1, '女'))
#     sex = models.PositiveSmallIntegerField(choices=sex_choices, blank=True, null=True)
#     old = models.IntegerField(blank=True,null=True)
#     grade =models.CharField(max_length=64,blank=True,null=True)
#     head_img = models.ImageField()
#
#     date = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name


class Box(models.Model):
    """箱柜信息"""
    box_name = models.CharField(max_length=32,blank=True,null=True,verbose_name="箱柜")
    use_date = models.CharField(max_length=64,blank=True,null=True,verbose_name="开放时间")


    def __str__(self):
        return self.box_name

    class Meta:
        verbose_name = "箱柜表"

class ChildBox(models.Model):
    """分柜信息"""

    boxnumber = models.ForeignKey("Box",blank=True,null=True,verbose_name="所属箱柜")
    child_name = models.CharField(max_length=16,blank=True,null=True,verbose_name="格子号")

    status_choices = ((0, '空闲'),
                      (1, '预定'),
                      )
    status = models.SmallIntegerField(choices=status_choices, default=0,verbose_name="当前状态")



    def __str__(self):
        return self.child_name

    class Meta:
        verbose_name = "分柜表"



class ReservationInfo(models.Model):
    """预约信息"""
    name = models.ForeignKey("UserProfile",blank=True,verbose_name="申请人")
    Box = models.ForeignKey("Box",blank=True,verbose_name="箱柜")
    number = models.ForeignKey("ChildBox",blank=True,verbose_name="格子")
    status_choices = ((0, '审核中'),
                      (1, '通过'),
                      (2, '退订'),
                      (3, '过期'),
                      )
    status = models.SmallIntegerField(choices=status_choices,default=0,verbose_name="状态")
    startdate = models.DateField(blank=True,null=True,verbose_name="开始时间")
    enddate = models.DateField(blank=True,null=True,verbose_name="结束时间")



    class Meta:
        verbose_name = "预约信息表"


class Menus(models.Model):
    """动态菜单"""
    name = models.CharField(max_length=64)
    url_type_choices = ((0,'absolute'),(1,'dynamic'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name','url_name')
        verbose_name = "菜单表"
