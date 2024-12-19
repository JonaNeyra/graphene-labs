import graphene
from graphene_django.types import DjangoObjectType

from .models import Patient, MedicalHistory


class PatientType(DjangoObjectType):
    class Meta:
        model = Patient


class MedicalHistoryType(DjangoObjectType):
    class Meta:
        model = MedicalHistory


class Query(graphene.ObjectType):
    all_patients = graphene.List(PatientType)
    records_by_patient = graphene.List(MedicalHistoryType, patient_id=graphene.Int())

    def resolve_all_patients(self, info):
        return Patient.objects.prefetch_related('records').all()

    def resolve_records_by_patient(self, info, patient_id):
        return MedicalHistory.objects.filter(patient_id=patient_id)


schema = graphene.Schema(query=Query)
