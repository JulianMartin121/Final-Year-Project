from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

# Custom User model, the two types will be student and teacher
class CustomUser(AbstractUser): 
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'teacher'),
    )

    # Field to distinguish between student and teacher
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)

    # Field to store the University ID
    Uni_ID = models.CharField(max_length=10, default='')

    # Email field
    email = models.EmailField(_('email address'), unique=True)

    # Override the groups field to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set",
        related_query_name="user",
    )

    # Override the user_permissions field to avoid reverse accessor clashes
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="user",
    )

