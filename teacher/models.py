from django.db import models
from django.conf import settings
from department.models import Department, Office


class TeacherInfo(models.Model):

    t_id = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='工号',
                                on_delete=models.CASCADE, primary_key=True,
                                limit_choices_to={'groups__name': 'teachers'})
    t_department = models.ForeignKey(Department, verbose_name='院系',
                                     on_delete=models.SET_NULL, blank=True,
                                     null=True)
    t_office = models.ForeignKey(Office, verbose_name='教研室',
                                 on_delete=models.SET_NULL, blank=True,
                                 null=True)
    t_title = models.CharField('职称', max_length=10)
    t_contact = models.CharField('联系方式', max_length=20, default='无')
    t_maxchoice = models.IntegerField('可选人数', default=5)

    @property
    def get_set(self):
        return self.studentinfo_set.values()

    def get_choosed(self):
        return len(self.get_set)
    get_choosed.short_description = '已选人数'

    def get_confirmed(self):
        count = 0
        for i in self.get_set:
            if i['s_isconfirm']:
                count += 1
        return count
    get_confirmed.short_description = '已确认人数'

    def get_name(self):
        return self.t_id.first_name
    get_name.short_description = '姓名'
    get_name.admin_order_field = 't_id__first_name'

    class Meta:
        verbose_name = '教师信息'
        verbose_name_plural = '教师信息'
        ordering = ['t_id']
        permissions = (('is_teacher', 'is a teacher'),)

    def __str__(self):
        return self.t_id.first_name
