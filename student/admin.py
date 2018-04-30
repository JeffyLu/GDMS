from django.contrib import admin
from department.views import get_department
from department.models import Major
from student.models import StudentInfo
from teacher.models import TeacherInfo


# 学生
class StudentInfoAdmin(admin.ModelAdmin):

    list_display = ['s_id', 'get_name', 's_department', 's_major', 's_year',
                    's_contact', 's_teacher', 's_isconfirm']
    fieldsets = [
        (
            None,
            {'fields': ['s_id', 'get_name']},
        ),
        (
            '个人信息',
            {'fields': ['s_department', 's_major', 's_year', 's_contact']},
        ),
        (
            '导师',
            {'fields': ['s_teacher', 's_isconfirm']},
        ),
    ]

    def get_search_fields(self, request):
        if request.user.is_superuser:
            search_fields = ['s_id__first_name', 's_id__username',
                             's_department__name', 's_major__name',
                             's_year__value', 's_teacher__t_id__first_name']
        elif request.user.has_perm('department.is_manager'):
            search_fields = ['s_id__first_name', 's_id__username',
                             's_major__name', 's_year__value',
                             's_teacher__t_id__first_name']
        else:
            search_fields = []
        return search_fields

    def get_list_filter(self, request):
        if request.user.is_superuser:
            list_filter = ['s_department', 's_isconfirm']
        elif request.user.has_perm('department.is_manager'):
            list_filter = ['s_isconfirm']
        else:
            list_filter = []
        return list_filter

    def get_queryset(self, request):
        qs = super(StudentInfoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm('department.is_manager'):
            return qs.filter(s_department=request.user.manager.m_department)
        return qs.filter(s_id=request.user)

    def get_readonly_fields(self, request, obj):
        if request.user.is_superuser:
            mylist = ['get_name']
        elif request.user.has_perm('department.is_manager'):
            mylist = ['s_id', 'get_name', 's_isconfirm', 's_department']
        else:
            mylist = ['s_id', 'get_name', 's_department', 's_major', 's_year',
                      's_teacher', 's_isconfirm']
        return mylist

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        department = get_department(request)
        if department is not None:
            if db_field.name == 's_major':
                kwargs['queryset'] = Major.objects.filter(
                    department=department)
            if db_field.name == 's_teacher':
                kwargs['queryset'] = TeacherInfo.objects.filter(
                    t_department=department)
        return super(StudentInfoAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


admin.site.register(StudentInfo, StudentInfoAdmin)
