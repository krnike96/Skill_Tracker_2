from django import forms
from .models import Skill

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'proficiency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'proficiency': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'type': 'range',
            }),
        }