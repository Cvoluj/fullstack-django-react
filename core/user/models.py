from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from core.abstract.models import AbstractModel, AbstractManager


class UserManager(BaseUserManager, AbstractManager):

    def create_user(self, username, email, password=None, **kwargs):
        """
        Create and return a `User` with an email, phone,
        number, username and password.
        """
        if username is None:
            raise TypeError('User must have a username.')
        if email is None:
            raise TypeError('User must have an email.')
        if password is None:
            raise TypeError('User must have an email.')

        user: User = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **kwargs):
        """
        Create and return `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have a username.')
        if email is None:
            raise TypeError('Superusers must have an email.')

        user: User = self.create_user(username=username, email=email, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    posts_liked = models.ManyToManyField('core_post.Post', related_name='liked_by')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def like(self, post):
        """
        Like `post` if it hasn't been done yet
        """
        return self.posts_liked.add(post)

    def remove_like(self, post):
        """
        Remove a like from a `post`
        """
        return self.posts_liked.remove(post)

    def has_liked(self, post):
        """
        Return True if user has liked a `post`; else False
        """
        return self.posts_liked.first(pk=post.pk).exists()

    def __str__(self):
        return f'{self.email}'

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
# Create your models here.
