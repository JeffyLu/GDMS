from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from student.models import StudentInfo
from department.models import Time


# 开放年级
def available_years(request):
    try:
        times = Time.objects.filter(
            department=request.user.teacherinfo.t_department
        )
        return [t.year for t in times if t.is_available_time]
    except AttributeError:
        return []


# 我的学生
@login_required
@staff_member_required(login_url='login')
def my_student(request):
    if request.method == 'POST':
        s_user = User.objects.get(username=request.POST['student'])
        student = StudentInfo.objects.get(s_id=s_user)
        if 'confirm' in request.POST:
            student.s_isconfirm = True
        if 'cancel' in request.POST:
            student.s_isconfirm = False
        student.save()
        return HttpResponseRedirect('./my_student')
    try:
        students = request.user.teacherinfo.studentinfo_set.all()
    except AttributeError:
        students = None

    context = {
        'students': students,
        'available_years': available_years(request),
    }
    return render(request, 'my_student.html', context)
