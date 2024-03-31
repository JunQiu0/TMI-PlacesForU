from django import forms
 
class UploadImageForm(forms.Form):
    image_field = forms.ImageField(label='')#image')