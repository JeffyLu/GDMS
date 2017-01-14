from django.shortcuts import render
from django.http import HttpResponseRedirect
from student.models import StudentInfo
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from department.models import *
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.


#开放年级
def available_years(request):
    try:
        time = Time.objects.filter(
            department = request.user.teacherinfo.t_department
        )
        print([t for t in time if t.is_available_time])
        return [t.year for t in time if t.is_available_time]
    except:
        return []


#我的学生
@login_required
@staff_member_required(login_url = 'login')
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

    except:
        students = None

    context = {
        'students' : students,
        'available_years' : available_years(request),
    }

    return render(request, 'my_student.html', context)
