#post方法提交表单的基本框架
def post_func(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
            '''
            do something
            '''
        #请求数据合法
        if form.is_valid():
            '''
            do something
            '''
            #提交后跳转或者其他
            return 
    else:
        form = MyForm()
    context = {
        'form' : form,
    }
    return render(request, 'template.html', context)
    
    
'''
template.html

<form action="redrict" method="post">
{% csrf_token %}
{{ form }}
<input type="submit" value="submit" />
</form>
'''
