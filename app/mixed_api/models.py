"""
Models for Medical History
"""
from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=255)
    years = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class MedicalHistory(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='records',
    )
    date = models.DateField()
    diagnostic = models.TextField()

    def __str__(self):
        return f'{self.date} - {self.patient.name}'
