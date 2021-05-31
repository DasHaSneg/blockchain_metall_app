from django import forms
from .models import Company, ContractTemplate


class TemplateRecallForm(forms.Form):
    diplom_file = forms.FileField(required=True, label="", widget=forms.FileInput(
        attrs={'style': 'display: none;', 'accept': 'application/json'}))


class ContractTemplateCreateForm(forms.Form):
    buyer = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class': 'myfield'}),
                                   queryset=Company.objects.all(), label="Покупатель")
    supplier = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class': 'myfield'}),
                                      queryset=Company.objects.all(), label="Поставщик")


class ContractTemplateSignForm(forms.Form):
    user_template = forms.ModelChoiceField(required=True, widget=forms.Select(attrs={'class': 'myfield'}),
                                           queryset=ContractTemplate.objects.all(), label="Шаблон контракта")
    roster = forms.FileField(required=True, label="",
                             widget=forms.FileInput(attrs={'style': 'display: none;', 'accept': '.csv'}))

    def __init__(self, temp_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_template'].queryset = ContractTemplate.objects.filter(user_id__exact=temp_user.id)
