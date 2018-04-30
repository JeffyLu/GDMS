import xlrd

from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import login
from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError

from student.models import StudentInfo
from teacher.models import TeacherInfo
from notice.models import Notice
from department.models import Department, Office, Major, Year
from department.views import get_department


# 登录限制
def limited_login(request):
    if 'username' in request.POST:
        username = request.POST['username']
        user = User.objects.filter(username=username).first()
    else:
        user = None

    if user is not None and user.username in request.session:
        if not user.is_superuser and request.session[user.username] >= 3:
            user.is_staff = False
            user.save()
            return HttpResponse('密码输入错误3次, 账户已锁定!')

    rep = login(request)
    status_code = rep.status_code
    if status_code == 200 and user is not None:
        if user.username in request.session:
            request.session[user.username] += 1
        else:
            request.session[user.username] = 1
    return rep


# 首页
@login_required
@staff_member_required(login_url='login')
def index(request):
    department = get_department(request)
    if department is not None:
        latest_notice = Notice.objects.filter(
            department=department).order_by('-pub_date')[:3]
    else:
        latest_notice = Notice.objects.order_by('-pub_date')[:3]

    context = {'latest_notice': latest_notice}
    return render(request, 'index.html', context)


# 获取表格
def get_xls_table(sheet_name):
    try:
        data = xlrd.open_workbook('GDMS/data.xls')
    except Exception:
        return None
    return data.sheet_by_name(sheet_name)


# 行迭代生成器
def get_xls_line(sheet_name):
    table = get_xls_table(sheet_name)
    if table is None:
        return None
    for r in range(1, table.nrows):
        yield table.row_values(r)


# 添加学院、专业、教研室、年级
def add_basis():
    s_table = get_xls_table('students')
    t_table = get_xls_table('teachers')
    s_department = s_table.col_values(0)[1:]
    t_department = t_table.col_values(0)[1:]
    department = s_department + t_department
    office = t_table.col_values(1)[1:]
    major = s_table.col_values(1)[1:]
    year = s_table.col_values(2)[1:]

    for d in set(department):
        try:
            Department.objects.create(name=d)
        except IntegrityError:
            continue

    for o in set(zip(t_department, office)):
        try:
            Office.objects.create(
                department=Department.objects.get(name=o[0]),
                name=o[1],
            )
        except IntegrityError:
            continue

    for m in set(zip(s_department, major)):
        try:
            Major.objects.create(
                department=Department.objects.get(name=m[0]),
                name=m[1]
            )
        except IntegrityError:
            continue

    for y in set(year):
        try:
            Year.objects.create(value=int(y))
        except IntegrityError:
            continue


# 添加教师
def add_teachers():
    values = get_xls_line('teachers')
    if values is None:
        return False

    for line in values:
        (department, office, username, name, title, contact, maxchoice) = line

        try:
            teacher = User.objects.create_user(
                username=username,
                password='asdfasdfasdf',
                first_name=name,
            )
        except IntegrityError:
            teacher = User.objects.get(username=username)
        finally:
            teacher.is_staff = True
            teacher.groups.add(Group.objects.get(name='teachers'))
            teacher.save()

        try:
            TeacherInfo.objects.create(
                t_id=teacher,
                t_department=Department.objects.get(name=department),
                t_office=Office.objects.get(name=office),
                t_title=title,
                t_contact=contact,
                t_maxchoice=int(maxchoice),
            )
        except IntegrityError:
            pass


# 添加学生
def add_students():
    values = get_xls_line('students')
    if values is None:
        return False

    for line in values:
        (department, major, year, username, name, contact) = line

        try:
            student = User.objects.create_user(
                username=username,
                password='asdfasdfasdf',
                first_name=name,
            )
        except IntegrityError:
            student = User.objects.get(username=username)
        finally:
            student.is_staff = True
            student.groups.add(Group.objects.get(name='students'))
            student.save()

        try:
            StudentInfo.objects.create(
                s_id=student,
                s_department=Department.objects.get(name=department),
                s_major=Major.objects.get(name=major),
                s_year=Year.objects.get(value=year),
                s_contact=contact,
            )
        except IntegrityError:
            pass


# 导入数据
@permission_required('is_superuser')
def add(request):
    add_basis()
    add_teachers()
    add_students()
    return render(request, 'index.html')
