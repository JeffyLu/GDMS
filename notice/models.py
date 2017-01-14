from django.db import models
from department.models import *
# Create your models here.

class Notice(models.Model):

    department = models.ForeignKey(
        Department,
        verbose_name = '学院',
        on_delete = models.CASCADE,
    )

    title = models.CharField(
        '标题',
        max_length = 20,
    )

    detail = models.TextField(
        '详细内容',
        max_length = 1000,
    )

    pub_date = models.DateTimeField(
        '发布时间',
        auto_now_add = True,
    )

    def get_bref(self):
        return self.detail[:50]
    get_bref.short_description = '概要'

    class Meta:

        verbose_name = '公告'
        verbose_name_plural = '公告'

    def __str__(self):

        return self.title

