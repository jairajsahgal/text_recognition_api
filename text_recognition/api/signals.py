from os import access
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Account

@receiver(post_delete,sender=Account)
def delete_user(sender,instance,*args,**kwargs):
    try:
        instance.user.delete()
    except Exception as e:
        print("User account already deleted!")