
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    appointment_date = models.DateTimeField()

    reason = models.TextField()

    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[FileExtensionValidator(['pdf'])]
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    duration_minutes = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    def clean(self):
        super().clean()

        # Vérifier la date uniquement lors de la création
        # ou lorsque la date du rendez-vous est modifiée.
        if self.appointment_date:
            if self.pk is None:
                if self.appointment_date <= timezone.now():
                    raise ValidationError({
                        'appointment_date':
                        "La date du rendez-vous doit être dans le futur."
                    })
            else:
                old_date = Appointment.objects.filter(
                    pk=self.pk
                ).values_list('appointment_date', flat=True).first()

                if old_date != self.appointment_date:
                    if self.appointment_date <= timezone.now():
                        raise ValidationError({
                            'appointment_date':
                            "La nouvelle date doit être dans le futur."
                        })

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date'
            )
        ]

        ordering = ['appointment_date']

    def __str__(self):
        return f"{self.doctor} - {self.appointment_date}"
