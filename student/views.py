from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.admin.views.decorators import staff_member_required

from teacher.models import TeacherInfo
from department.models import Time
from department.views import get_department


# 获取系统开放状态
def system_is_available(request):
    try:
        time = Time.objects.get(
            department=request.user.studentinfo.s_department,
            year=request.user.studentinfo.s_year,
        )
        return time.is_available_time
    except Time.DoesNotExist:
        return None


# 导师选择
@login_required
@staff_member_required(login_url='login')
def choose_teacher(request):
    if request.method == 'POST':
        t_user = User.objects.get(username=request.POST['teacher'])
        teacher = TeacherInfo.objects.get(t_id=t_user)
        request.user.studentinfo.s_teacher = teacher
        request.user.studentinfo.save()
        return HttpResponseRedirect('/student/my_teacher')

    department = get_department(request)
    if department is not None:
        teacher_list = TeacherInfo.objects.filter(t_department=department)
    elif request.user.is_superuser:
        teacher_list = TeacherInfo.objects.all()
    else:
        teacher_list = []

    paginator = Paginator(teacher_list, 10)
    page = request.GET.get('page')
    try:
        teachers = paginator.page(page)
    except PageNotAnInteger:
        teachers = paginator.page(1)
    except EmptyPage:
        teachers = paginator.page(paginator.num_pages)

    context = {
        'teachers': teachers,
        'system_is_available': system_is_available(request),
    }
    return render(request, 'choose_teacher.html', context)


# 我的导师
@login_required
@staff_member_required(login_url='login')
def my_teacher(request):
    if request.method == 'POST':
        request.user.studentinfo.s_teacher = None
        request.user.studentinfo.s_isconfirm = False
        request.user.studentinfo.save()
    try:
        teacher = request.user.studentinfo.s_teacher
        status = '是' if request.user.studentinfo.s_isconfirm else '否'
    except AttributeError:
        teacher = None
        status = None

    context = {
        'teacher': teacher,
        'status': status,
        'system_is_available': system_is_available(request),
    }
    return render(request, 'my_teacher.html', context)
