from django.db import models
from django.utils.text import slugify 
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

# Create your models here.
class UploadImageModel(models.Model):
	title=models.CharField(max_length=200)
	img=models.ImageField(upload_to="images/")

	def __str__(self):
		return self.title
      
@receiver(post_delete, sender=UploadImageModel)
def eliminar_archivo_de_imagen(sender, instance, **kwargs):
    # Eliminar el archivo de imagen asociado
    if instance.img:
        if os.path.exists(instance.img.path):
            os.remove(instance.img.path)