from django import forms


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=25)


class CategoryIdForm(forms.Form):
    id = forms.IntegerField()