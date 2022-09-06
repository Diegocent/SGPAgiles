from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError('El usuario debe proveer un email!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save()
        return user

    def create_superuser(self, email, **extra_fields):
        extra_fields['rol'] = 'admin'
        extra_fields['is_active'] = True
        return self.create_user(email, **extra_fields)