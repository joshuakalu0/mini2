from django.db import models
from shortuuid.django_fields import ShortUUIDField



class Organisation(models.Model):
	orgId= ShortUUIDField( length=11, max_length=11,unique=True)
	name= models.CharField(max_length=225)
	description =models.TextField()
# Create your models here.