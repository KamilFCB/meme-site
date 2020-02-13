from django import forms


class UploadImageForm(forms.Form):
    title = forms.CharField(max_length=30)
    image = forms.ImageField()
