from django.db import models
from django.contrib.auth.models import AbstractUser


# Make the User only for future possible uses
class User(AbstractUser):
    pass
