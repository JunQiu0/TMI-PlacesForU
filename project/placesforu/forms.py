from django import forms
 
class UploadImageForm(forms.Form):
    image_url = forms.CharField(label='Sube una imagen')
    image_url.required = False
    image_field = forms.ImageField(label='')#image')
    image_field.required = False