from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password=None, **extra_fields):
        '''create and saves new user'''
        user = self.model
