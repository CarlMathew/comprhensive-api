from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email = None, password = None, role = "user"):
        if not username:
            raise ValueError("Please provide the username")
        email = self.normalize_email(email)
        user = self.model(username = username, email = email, role = role)
        user.set_password(password)
        user.save(using = self.db)

class Users(AbstractBaseUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
        ("manager", "Manager")
    )


    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    role = models.CharField(max_length=200, choices=ROLE_CHOICES, default="user")
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["emails"]


    def __str__(self):
        return f"{self.username}: {self.role}"