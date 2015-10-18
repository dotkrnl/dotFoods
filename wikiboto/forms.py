from django import forms

class NewRootForm(forms.Form):
    new_root = forms.URLField(label='URL')
    depth = forms.IntegerField(min_value=1, max_value=10, label='Depth')
