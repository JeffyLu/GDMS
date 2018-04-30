from django.contrib import admin
from teacher.models import TeacherInfo
from student.models import StudentInfo
from department.models import Office
from department.views import get_department


class TeacherInfoInline(admin.TabularInline):

    model = StudentInfo
    extra = 0
    verbose_name_plural = '我的学生'

    fields = ['s_id', 's_department', 's_major', 's_year', 's_contact',
              's_isconfirm']

    def get_readonly_fields(self, request, obj):
        if request.user.is_superuser:
            mylist = []
        else:
            mylist = ['s_id', 'get_name', 's_department', 's_major', 's_year',
                      's_contact', 's_isconfirm']
        return mylist


class TeacherInfoAdmin(admin.ModelAdmin):

    inlines = [TeacherInfoInline]

    list_display = ['t_id', 'get_name', 't_department', 't_office', 't_title',
                    't_contact', 't_maxchoice', 'get_choosed', 'get_confirmed']
    fieldsets = [
        (
            None,
            {'fields': ['t_id', 'get_name']},
        ),
        (
            '毕业设计管理',
            {'fields': ['t_maxchoice', 'get_choosed', 'get_confirmed']},
        ),
        (
            '个人信息',
            {'fields': ['t_department', 't_office', 't_title', 't_contact']},
        ),
    ]

    def get_search_fields(self, request):
        basic_fields = ['t_id__username', 't_id__first_name',
                        't_office__name', 't_title']
        if request.user.is_superuser:
            search_fields = basic_fields
            search_fields.append('t_department__name')
        elif request.user.has_perm('department.is_manager'):
            search_fields = basic_fields
        else:
            search_fields = []
        return search_fields

    def get_list_filter(self, request):
        if request.user.is_superuser:
            list_filter = ['t_department', 't_maxchoice']
        elif request.user.has_perm('department.is_manager'):
            list_filter = ['t_maxchoice']
        else:
            list_filter = []
        return list_filter

    def get_queryset(self, request):
        qs = super(TeacherInfoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm('department.is_manager'):
            return qs.filter(t_department=request.user.manager.m_department)
        return qs.filter(t_id=request.user)

    def get_readonly_fields(self, request, obj):
        if request.user.is_superuser:
            mylist = ['get_name', 'get_choosed', 'get_confirmed']
        else:
            mylist = ['t_id', 'get_name', 't_department', 'get_choosed',
                      'get_confirmed']
        return mylist

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        department = get_department(request)
        if department is not None:
            if db_field.name == 't_office':
                kwargs['queryset'] = Office.objects.filter(
                    department=department,
                )
        return super(TeacherInfoAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


admin.site.register(TeacherInfo, TeacherInfoAdmin)
