from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Company


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):                                      
        if username is None:
            raise ValueError(_('User should have a username'))
        if password is None:
            raise ValueError(_('Password should not be none'))
        if email is None:
            raise ValueError(_('User should have a Email'))

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)      
        user.save()                                                                           
        return user                                                                            

    def create_superuser(self, username, email, password=None):                                 
        user = self.create_user(username, email, password, )
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.is_active = True
        user.is_employer = True
        user.is_seeker = False
        user.save()                                                                             
        return user                                                                            


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)                     
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)                                            
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=True)
    is_employer = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add =True)                                        
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'                                                                   
    REQUIRED_FIELDS = ['username']                                                              

    objects = UserManager()                                                                     

    def __str__(self):
        return self.email



