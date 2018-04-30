from django.contrib import admin
from notice.models import Notice
from department.views import get_department
from department.models import Department


class NoticeAdmin(admin.ModelAdmin):

    search_fields = ['title', 'department__name']
    list_display = ['title', 'get_bref', 'pub_date', 'department']

    def get_queryset(self, request):
        qs = super(NoticeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm('department.is_manager'):
            return qs.filter(department=request.user.manager.m_department)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        department = get_department(request)
        if department is not None:
            if db_field.name == 'department':
                kwargs['initial'] = department
                kwargs['queryset'] = Department.objects.filter(
                    name=department.name
                )
        return super(NoticeAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


admin.site.register(Notice, NoticeAdmin)
