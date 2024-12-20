import graphene
from django.db.models import Q
from graphene_django.types import DjangoObjectType

from .models import Appointment, Patient, Doctor


class DoctorType(DjangoObjectType):
    class Meta:
        model = Doctor


class PatientType(DjangoObjectType):
    class Meta:
        model = Patient


class AppointmentType(DjangoObjectType):
    class Meta:
        model = Appointment


class CreateDoctor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        specialty = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, name, specialty):
        registred_doctor = Doctor.objects.filter(
            name=name,
            specialty=specialty,
        )

        if registred_doctor.exists():
            return CreateDoctor(success=False, message="The doctor exists")

        Doctor.objects.create(
            name=name,
            specialty=specialty
        )

        return CreateDoctor(success=True, message="Doctor created")


class CreatePatient(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        has_debts = graphene.Boolean()

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, name, has_debts):
        registred_patient = Patient.objects.filter(
            name=name
        )

        if registred_patient.exists():
            return CreatePatient(success=False, message="The patient exists")

        Patient.objects.create(
            name=name,
            has_debts=has_debts,
        )

        return CreatePatient(success=True, message="Patient created")


class CreateAppointment(graphene.Mutation):
    class Arguments:
        patient_id = graphene.Int(required=True)
        doctor_id = graphene.Int(required=True)
        date = graphene.Date(required=True)
        from_time = graphene.Time(required=True)
        to_time = graphene.Time(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, patient_id, doctor_id, date, from_time, to_time):
        registred_appointment = Appointment.objects.filter(
            Q(from_time__lt=to_time, to_time__gt=from_time),
            doctor_id=doctor_id,
            date=date,
        )

        if registred_appointment.exists():
            return CreateAppointment(
                success=False,
                message="Time Conflict",
            )

        patient = Patient.objects.get(id=patient_id)
        if hasattr(patient, 'has_debts') and patient.has_debts:
            return CreateAppointment(
                success=False,
                message="This patient has debts",
            )

        doctor = Doctor.objects.get(id=doctor_id)
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            from_time=from_time,
            to_time=to_time,
            status="Confirmed"
        )

        return CreateAppointment(
            success=True,
            message="Appointment created",
        )


class Query(graphene.ObjectType):
    all_doctors = graphene.List(DoctorType)
    all_patients = graphene.List(PatientType)
    patient = graphene.Field(PatientType, patient_id=graphene.Int())

    def resolve_all_doctors(self, info):
        return Doctor.objects.all()

    def resolve_all_patients(self, info):
        return Patient.objects.all()

    def resolve_patient(self, info, patient_id):
        return Patient.objects.get(pk=patient_id)


class Mutation(graphene.ObjectType):
    create_appointment = CreateAppointment.Field()
    create_doctor = CreateDoctor.Field()
    create_patient = CreatePatient.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
