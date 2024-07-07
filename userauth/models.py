
from django.db import models
from django.contrib.auth.models import (
   AbstractUser
)

from shortuuid.django_fields import ShortUUIDField
from organisation.models  import Organisation
# Create your models here.

class User(AbstractUser):
    userId= ShortUUIDField( length=11, max_length=11,unique=True)
    email = models.EmailField(unique=True,max_length=225)
    firstName = models.CharField(max_length=225,null=False,blank=False)
    lastName = models.CharField(max_length=225,null=False,blank=False)
    username = models.CharField(unique=True,max_length=225)
    phone = models.CharField(max_length=12,null=False,blank=False)
    organisation = models.ManyToManyField(Organisation,blank=True)




    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return f'{self.firstName} - {self.email}'

    # def save(self, *arg, **kwargs):

    #     return super(User,self).save( *arg, **kwargs)