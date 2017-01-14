from django.db import models
from django.conf import settings
from teacher.models import TeacherInfo
from department.models import *
# Create your models here.

class StudentInfo(models.Model):

    s_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name = '学号',
        on_delete = models.CASCADE,
        primary_key = True,
        limit_choices_to = {'groups__name' : 'students'},
    )

    s_department = models.ForeignKey(
        Department,
        verbose_name = '院系',
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
    )

    s_major = models.ForeignKey(
        Major,
        verbose_name = '专业',
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
    )

    s_year = models.ForeignKey(
        Year,
        verbose_name = '年级',
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
    )

    s_contact = models.CharField(
        '联系方式',
        max_length = 20,
        default = '无',
    )

    s_teacher = models.ForeignKey(
        TeacherInfo,
        verbose_name = '导师',
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
    )

    s_isconfirm = models.BooleanField(
        '导师确认',
        default = False,
    )

    def get_name(self):
        return self.s_id.first_name
    get_name.short_description = '姓名'
    get_name.admin_order_field = 's_id__first_name'

    class Meta:

        verbose_name = '学生资料'
        verbose_name_plural = '学生资料'
        ordering = ['s_id']
        permissions = (
            ('is_student', 'is a student'),
        )

    def __str__(self):

        return self.s_id.first_name


