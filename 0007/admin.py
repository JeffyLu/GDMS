#后台的一些定制

from django.contrib import admin
import model1, model2

#显示外键
class model1Inline(admin.StackedInline):
    
    model = model2
    
    #添加额外空外键
    extra = 0
    
    #显示名称
    verbose_name = '学号'
    verbose_name_plural = '我的学生'
    
    #只读属性
    readonly_fields = [ ]
    
class model1Admin(admin.ModelAdmin):
    
    #显示外键
    inlines = [model1Inline]
    
    #显示列表
    list_display = ['属性',]

    #搜索域
    search_fields = ['属性', '外键__属性',]

    #过滤属性
    list_filter = [
        '属性',
    ]

    #列表中除超级用户外只显示自己
    def get_queryset(self, request):
        qs = super(StudentInfoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(s_id = request.user)

    #获取只读属性
    def get_readonly_fields(self, request, obj):
        if request.user.is_superuser:
            #非库内字段必须返回只读
            mylist = ['get_xxx',]
        else:
            mylist = ['属性',]
        return mylist

    #修改界面块
    fieldsets = [
        ('块名', {'fields' : ['属性', '属性']}),
        ('块名', {'fields' : ['属性', '属性',]}),
    ]


admin.site.register(moedl1, model1Admin)

