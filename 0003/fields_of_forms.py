#基本表单属性
from django import forms

class MyForm(forms.Form):
    age = forms.IntegerField(
        label = '年龄',
        min_value = 1,
        max_value = 100,
        widget = forms.NumberInput(
            attrs = {
                'placeholder':'1-150岁',
                'size':'20',
                'title':'请填写年龄!',
            }
        ),
    )

    GENDER_CHOICE = (('男', '男'), ('女', '女'))
    gender = forms.CharField(
        widget = forms.Select(
            choices = GENDER_CHOICE
        ),
    )

    height = forms.DecimalField(
        #最大位数5,最大小数位2
        max_digits = 5,
        decimal_places = 2,
    )
    
    #干净数据处理
    def clean_age(self):
        age = self.cleaned_data['age']
        #输入无效
        if age <= 0 or age > 100:
            raise forms.ValidationError("请填写有效的年龄(1-150).")
        return age

