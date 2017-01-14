from django.shortcuts import render
from notice.models import Notice
from django.contrib.auth.decorators import login_required
from department.views import get_department
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.


@login_required
@staff_member_required(login_url = 'login')
def notice(request):

    department = get_department(request)
    if department is not None:
        notice_list = Notice.objects.filter(
            department = department
        ).order_by('-pub_date')
    else:
        notice_list = Notice.objects.order_by('-pub_date')

    paginator = Paginator(notice_list, 10)
    page = request.GET.get('page')
    try:
        notices = paginator.page(page)
    except PageNotAnInteger:
        notices = paginator.page(1)
    except EmptyPage:
        notices = paginator.page(paginator.num_pages)

    context = {
        'notices' : notices,
    }

    return render(request, 'notice.html', context)


@login_required
@staff_member_required(login_url = 'login')
def detail(request, nid):

    notice = Notice.objects.get(id=int(nid))

    context = {
        'notice' : notice,
    }

    return render(request, 'notice_detail.html', context)
