from django import forms
 
class UploadImageForm(forms.Form):
    #name = forms.CharField()
    image_field = forms.ImageField()