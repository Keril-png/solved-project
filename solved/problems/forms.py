from django import forms
from .models import Problem

class ProblemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False
        
    class Meta:
        model = Problem
        fields = ('title', 'description', 'file')
        labels ={
            'title':'Название',
            'description':'Текст задачи',
            'file':'Прикрепите файл',
        }