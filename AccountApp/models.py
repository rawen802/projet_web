
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone


# Modèle utilisateur personnalisé
class User(AbstractUser):
    pass


# Modèle Doctor
class Doctor(User):
    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)]
    )

    specialties = models.ManyToManyField('Specialty', blank=True)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


# Modèle Patient
class Patient(User):
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    birth_date = models.DateField()

    def clean(self):
        super().clean()
        if self.birth_date and self.birth_date >= timezone.localdate():
            from django.core.exceptions import ValidationError
            raise ValidationError({
                'birth_date': "La date de naissance doit être antérieure à aujourd'hui."
            })

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"


# Modèle Specialty
class Specialty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
