from appointments.models import Doctor, Patient
from appointments.schema import schema
from django.test import TestCase
from graphene.test import Client


class GrapheneTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(
            name="Dr. Strange",
            specialty="Surgery",
        )
        self.patient = Patient.objects.create(
            name="Jonathan Neyra",
            has_debts=False,
        )

    def test_create_doctor(self):
        client = Client(schema)
        mutation = """
        mutation {
            createDoctor(
                name: "Belen Mandujano Trejo",
                specialty: "Medico General"
            ) {
                success
                message
            }
        }
        """
        result = client.execute(mutation)
        self.assertTrue(result['data']['createDoctor']['success'])
        self.assertEqual(
            result["data"]["createDoctor"]["message"],
            "Doctor created",
        )

    def test_create_patient(self):
        client = Client(schema)
        mutation = """
        mutation {
            createPatient(name: "Jane Doe", hasDebts: true) {
                success
                message
            }
        }
        """
        result = client.execute(mutation)
        self.assertTrue(result["data"]["createPatient"]["success"])
        self.assertEqual(
            result["data"]["createPatient"]["message"],
            "Patient created",
        )

    def test_create_appointment(self):
        client = Client(schema)
        mutation = f"""
        mutation {{
            createAppointment(
                patientId: {self.patient.id},
                doctorId: {self.doctor.id},
                date: "2024-12-20",
                fromTime: "10:00:00",
                toTime: "11:00:00"
            ) {{
                success
                message
            }}
        }}
        """
        result = client.execute(mutation)
        self.assertTrue(result["data"]["createAppointment"]["success"])
        self.assertEqual(
            result["data"]["createAppointment"]["message"],
            "Appointment created",
        )

    def test_query_patient(self):
        client = Client(schema)
        query = f"""
        query {{
            patient(patientId: {self.patient.id}) {{
                id
                name
                hasDebts
            }}
        }}
        """
        result = client.execute(query)
        self.assertEqual(result["data"]["patient"]["name"], "Jonathan Neyra")
        self.assertFalse(result["data"]["patient"]["hasDebts"])

    def test_query_all_doctors(self):
        client = Client(schema)
        query = """
        query {
            allDoctors {
                id
                name
                specialty
            }
        }
        """
        result = client.execute(query)
        self.assertGreaterEqual(len(result["data"]["allDoctors"]), 1)
        self.assertEqual(
            result["data"]["allDoctors"][0]["name"],
            "Dr. Strange",
        )
