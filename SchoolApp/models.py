from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, fee=None, is_active=True, is_student=False,
                    is_teacher=False,
                    is_clerk=False, is_admin=False, is_staff=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)  # change user password
        user_obj.student = is_student
        user_obj.clerk = is_clerk
        user_obj.is_superuser = is_admin
        user_obj.is_staff = is_staff
        user_obj.fee_amount = 0
        user_obj.teacher = is_teacher
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_student(self, email, full_name=None, password=None):
        user = self.create_user(
            email, full_name=full_name, password=password, is_student=True
        )
        return user

    def create_teacher(self, email, full_name=None, password=None):
        user = self.create_user(
            email, full_name=full_name, password=password, is_teacher=True
        )
        return user

    def create_clerk(self, email, fullname=None, password=None):
        user = self.create_user(
            email, fullname=fullname, password=password, is_clerk=True
        )

    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    # last_name = models.CharField(max_length=255, blank=True, null=True)
    admin_no = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    current_class = models.CharField(max_length=255, blank=True, null=True)
    req_fee_amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_staff = models.BooleanField(default=False)  # staff user non superuser
    is_active = models.BooleanField(default=True)  # can login
    teacher = models.BooleanField(default=False)  # teacher
    is_superuser = models.BooleanField(default=False)  # superuser
    clerk = models.BooleanField(default=False)  # clerk
    student = models.BooleanField(default=False)  # student
    timestamp = models.DateTimeField(auto_now_add=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []  # ['full_name'] #python manage.py createsuperuser

    object = UserManager()

    def __str__(self):
        return self.full_name

    def get_username(self):
        return self.full_name

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_student(self):
        return self.student

    @property
    def is_teacher(self):
        return self.teacher

    @property
    def is_clerk(self):
        return self.clerk

    # @property
    # def is_active(self):
    #     return self.active


class Fee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fee_amount = models.DecimalField(max_digits=8, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    dated = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, default='description')

    # def __str__(self):
    #     return self.description or ''


class Assignment(models.Model):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()
    description = models.CharField(max_length=255, default='description')
    current_class = models.CharField(max_length=255, default='class')

    # def __str__(self):
    #     return self.description or ''
