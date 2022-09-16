from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """유저 매니저 정의"""
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("계정 이메일을 입력해주세요.")
        if not password:
            raise ValueError("비밀번호를 입력해주세요.")
        if not name:
            raise ValueError("이름을 입력해주세요.")

        user = self.model(
            email = email,
            password = password,
            name = name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email = email,
            password = password,
            name = name,
        )

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractUser):
    """유저 모델"""
    email = models.EmailField(verbose_name="이메일", max_length=120, unique=True)
    name = models.CharField(verbose_name="이름", max_length=20)
    date_joined = models.DateTimeField(auto_now_add=True)

    # status
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "users"