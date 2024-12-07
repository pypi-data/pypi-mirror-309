from django.contrib.auth.base_user import (
    AbstractBaseUser,
)
from django.contrib.auth.validators import (
    UnicodeUsernameValidator,
)
from django.db import (
    models,
)


class User(AbstractBaseUser):

    USERNAME_FIELD = "username"

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
