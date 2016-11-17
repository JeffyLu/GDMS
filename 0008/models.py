from django.conf import settings

class MyModel(models.Model):

    #一对一外键
    a = models.OneToOneField(
        #User表
        settings.AUTH_USER_MODEL,
        verbose_name = 'name',
        #删除时外键一起删除
        on_delete = models.CASCADE,
        primary_key = True,
        #过滤外键
        limit_choices_to = {'groups__name' : 'teachers'}
    )

    b = models.ForeignKey(
        Department,
        verbose_name = 'name',
        #删除时外键设为空
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
    )

    @property
    def get_set(self):
        return self.studentinfo_set.values()

    def get_confirmed(self):
        count = 0
        for i in self.get_set:
            if i['s_isconfirm']:
                count +=1
        return count
    get_confirmed.short_description = '已确认人数'

    #获取用户表中的姓名
    def get_name(self):
        return self.t_id.first_name
    get_name.short_description = '姓名'
    get_name.admin_order_field = 't_id__first_name'

    class Meta:

        verbose_name = '教师信息'
        verbose_name_plural = '教师信息'
        #默认排序
        ordering = ['t_id']
        #添加权限
        permissions = (
            ('is_teacher', 'is a teacher'),
        )


    def __str__(self):
        return self.t_id.first_name

