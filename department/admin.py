from django.contrib import admin
from department.models import *
from student.models import StudentInfo
from teacher.models import TeacherInfo
# Register your models here.

#学院
class DepartmentOfficeInline(admin.StackedInline):

    model = Office
    extra = 0

class DepartmentManagerInline(admin.StackedInline):

    model = Manager
    extra = 0

class DepartmentMajorInline(admin.StackedInline):

    model = Major
    extra = 0

class DepartmentAdmin(admin.ModelAdmin):

    inlines = [
        DepartmentMajorInline,
        DepartmentOfficeInline,
        DepartmentManagerInline,
    ]

    list_display = [
        'name',
        'get_office_count',
        'get_teacher_count',
        'get_student_count',
    ]

    search_fields = [
        'name',
    ]

admin.site.register(Department, DepartmentAdmin)


#教研室
class OfficeInline(admin.TabularInline):

    model = TeacherInfo
    extra = 0
    verbose_name_plural = '教研室成员'

    def get_readonly_fields(self, request, obj):

        if request.user.is_superuser:
            mylist = []

        else:
            mylist = [
                't_id',
                't_title',
                't_contact',
                't_maxchoice',
                't_department',
            ]

        return mylist

    fields = [
        't_id',
        't_title',
        't_department',
        't_contact',
        't_maxchoice',
    ]

class OfficeAdmin(admin.ModelAdmin):

    inlines = [OfficeInline]

    list_display = [
        'name',
        'department',
        'get_teacher_count',
    ]

    def get_search_fields(self, request):

        if request.user.is_superuser:
            search_fields = [
                'name',
                'department__name',
            ]

        else:
            search_fields = []

        return search_fields

    def get_list_filter(self, request):

        if request.user.is_superuser:
            list_filter = [
                'department',
            ]

        else:
            list_filter = []

        return list_filter

    def get_queryset(self, request):

        qs = super(OfficeAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs

        if request.user.has_perm('department.is_manager'):
            return qs.filter(department = request.user.manager.m_department)

    def get_readonly_fields(self, request, obj):

        if request.user.is_superuser:
            mylist = []

        else:
            mylist = ['department']

        return mylist

admin.site.register(Office, OfficeAdmin)


#专业
class MajorAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'department',
        'get_student_count',
    ]

    def get_search_fields(self, request):
        if request.user.is_superuser:
            search_fields = [
                'name',
                'department__name',
            ]

        else:
            search_fields = []

        return search_fields

    def get_list_filter(self, request):

        if request.user.is_superuser:
            list_filter = [
                'department',
            ]

        else:
            list_filter = []

        return list_filter

    def get_queryset(self, request):

        qs = super(MajorAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs

        if request.user.has_perm('department.is_manager'):
            return qs.filter(department = request.user.manager.m_department)

    def get_readonly_fields(self, request, obj):

        if request.user.is_superuser:
            mylist = []

        else:
            mylist = ['department']

        return mylist

admin.site.register(Major, MajorAdmin)


#年级
class YearAdmin(admin.ModelAdmin):

    list_display = [
        'value',
        'get_student_count',
    ]

    search_fields = ['value']

admin.site.register(Year, YearAdmin)


#学院管理员
class ManagerAdmin(admin.ModelAdmin):

    list_display = [
        'm_id',
        'get_name',
        'm_department',
        'm_contact',
    ]

    search_fields = [
        'm_id__first_name',
        'm_id__username',
        'm_department__name',
    ]

    list_filter = [
        'm_department__name',
    ]

admin.site.register(Manager, ManagerAdmin)


#系统开放时间
class TimeAdmin(admin.ModelAdmin):

    list_display = [
        'department',
        'year',
        'start_time',
        'end_time',
        'get_system_status',
    ]

    def get_queryset(self, request):

        qs = super(TimeAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            return qs

        if request.user.has_perm('department.is_manager'):
            return qs.filter(department = request.user.manager.m_department)

    def get_fields(self, request, obj):

        if request.user.is_superuser:
            fields = [
                'department',
                'year',
                'start_time',
                'end_time',
            ]

        else:
            fields = [
                'start_time',
                'end_time',
            ]

        return fields

admin.site.register(Time, TimeAdmin)
