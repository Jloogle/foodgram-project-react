from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError('Поле email не может быть пустым')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser'):
            return self.create_user(email, password, username, **extra_fields)
        raise ValueError('Superuser must have is_superuser=True.')
