from django.db import models
from django.conf import settings
import datetime
# Create your models here.

#学院
class Department(models.Model):

    name = models.CharField(
        '学院',
        max_length = 20,
        primary_key = True,
    )

    def get_office_count(self):
        return len(self.office_set.all())
    get_office_count.short_description = '教研室数量'

    def get_teacher_count(self):
        return len(self.teacherinfo_set.all())
    get_teacher_count.short_description = '教师人数'

    def get_student_count(self):
        return len(self.studentinfo_set.all())
    get_student_count.short_description = '学生人数'

    class Meta:

        verbose_name = '学院'
        verbose_name_plural = '学院'

    def __str__(self):

        return self.name


#教研室
class Office(models.Model):

    department = models.ForeignKey(
        Department,
        on_delete = models.CASCADE,
        verbose_name = '学院',
    )

    name = models.CharField(
        '教研室',
        max_length = 20,
        primary_key = True,
    )

    def get_teacher_count(self):
        return len(self.teacherinfo_set.all())
    get_teacher_count.short_description = '教研室人数'

    class Meta:

        verbose_name = '教研室'
        verbose_name_plural = '教研室'

    def __str__(self):

        return self.name


#年级
class Year(models.Model):

    value = models.DecimalField(
        '年级',
        max_digits = 4,
        decimal_places = 0,
        primary_key = True,
    )

    def get_student_count(self):
        return len(self.studentinfo_set.all())
    get_student_count.short_description = '学生人数'

    class Meta:

        verbose_name = '年级'
        verbose_name_plural = '年级'

    def __str__(self):

        return str(self.value)


#专业
class Major(models.Model):

    department = models.ForeignKey(
        Department,
        on_delete = models.CASCADE,
        verbose_name = '学院',
    )

    name = models.CharField(
        '专业',
        max_length = 20,
        primary_key = True,
    )

    def get_student_count(self):
        return len(self.studentinfo_set.all())
    get_student_count.short_description = '学生人数'

    class Meta:

        verbose_name = '专业'
        verbose_name_plural = '专业'

    def __str__(self):

        return self.name


#学院管理员
class Manager(models.Model):

    m_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name = '帐号',
        on_delete = models.CASCADE,
        primary_key = True,
        limit_choices_to = {'groups__name' : 'department_manager'},
    )

    m_department = models.ForeignKey(
        Department,
        verbose_name = '学院',
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
    )

    m_contact = models.CharField(
        '联系方式',
        max_length = 20,
        default = '无',
    )

    def get_name(self):
        return self.m_id.first_name
    get_name.short_description = '姓名'
    get_name.admin_order_field = 'm_id__first_name'

    class Meta:

        verbose_name = '管理员'
        verbose_name_plural = '管理员'
        permissions = (
            ('is_manager', 'is a manager'),
        )

    def __str__(self):

        return self.m_id.username


#系统开放时间管理
class Time(models.Model):

    department = models.ForeignKey(
        Department,
        on_delete = models.CASCADE,
        verbose_name = '学院',
    )

    year = models.ForeignKey(
        Year,
        on_delete = models.CASCADE,
        verbose_name = '年级',
    )

    start_time = models.DateTimeField(
        '开放时间',
        null = True,
        blank = True,
    )

    end_time = models.DateTimeField(
        '关闭时间',
        null = True,
        blank = True,
    )

#    #防止重复和非法日期区间
#    def save(self, *args, **kwargs):
#        try:
#            dp = Time.objects.get(department=self.department, year=self.year)
#            if dp:
#                dp.department = self.department
#                dp.year = self.year
#                dp.start_time = self.start_time
#                dp.end_time = self.end_time
#                dp.save()
#                return True
#            if self.start_time >= self.end_time:
#                return False
#            else:
#                super(Time, self).save(*args, **kwargs)
#        except:
#            super(Time, self).save(*args, **kwargs)

    def get_system_status(self):
        if self.is_available_time:
            return '系统开放中'
        else:
            return '系统未开放'
    get_system_status.short_description = '系统状态'

    @property
    def is_available_time(self):
        try:
            now = datetime.datetime.now()
            start = self.start_time.replace(tzinfo = None)
            end = self.end_time.replace(tzinfo = None)
        except:
            return False
        if now > end or now < start:
            return False
        else:
            return True

    class Meta:

        verbose_name = '系统开放时间'
        verbose_name_plural = '系统开放时间'

    def __str__(self):

        return self.department.name + str(self.year.value) + '级'
