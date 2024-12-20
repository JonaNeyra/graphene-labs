from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=255)
    has_debts = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'{self.name} - {self.specialty}'


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return f'Appointment with {self.doctor.name} for {self.patient.name}'
