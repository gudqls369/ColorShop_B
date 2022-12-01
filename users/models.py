from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from image_optimizer.fields import OptimizedImageField

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=20,
        unique=True,
        error_messages={'unique': "이미 존재하는 유저네임입니다."}
    )
    bio = models.CharField(max_length=255, default='', blank=True)
    profile_img = OptimizedImageField(
        upload_to="uploads/%Y/%m/%d",
        optimized_image_output_size=(300, 300),
        optimized_image_resize_method="cover",  #  "crop", "cover", "contain", "width", "height", "thumbnail" or None
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    nickname = models.CharField(max_length=30, default="", unique=True, error_messages={'unique': "이미 존재하는 닉네임입니다."})

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin