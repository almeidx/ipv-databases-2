from django import forms


class LanguageForm(forms.Form):
    name = forms.CharField(max_length=20)


class LanguageIdForm(forms.Form):
    id = forms.IntegerField()
