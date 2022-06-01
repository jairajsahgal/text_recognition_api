from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
def nameFile(instance, filename):
    return '/'.join(['images', filename])

class Account(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100,blank=False,null=False,unique=True)
    email = models.EmailField(max_length=100,blank=False,null=False,unique=True)

    def __str__(self) -> str:
        return self.username


class Picture(models.Model):
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=nameFile,null=True,blank=True,max_length=100)
    text = models.TextField(max_length=1000,blank=True,null=True,default="Not found!")