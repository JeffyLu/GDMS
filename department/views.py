def get_department(request):
    '''获取当前用户所在学院'''

    try:
        if request.user.has_perm('student.is_student'):
            return request.user.studentinfo.s_department
        elif request.user.has_perm('teacher.is_teacher'):
            return request.user.teacherinfo.t_department
        elif request.user.has_perm('department.is_manager'):
            return request.user.manager.m_department
        else:
            return None
    except Exception:
        return None
