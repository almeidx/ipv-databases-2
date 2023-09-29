from django import forms


class LanguageForm(forms.Form):
    name = forms.CharField(max_length=20)
