from django.test import TestCase
from graphene.test import Client
from policies.models import Agent, User, Policy, Dependent
from policies.schema import schema


class PoliciesTest(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(name="Belen Mandujano")
        self.user = User.objects.create(name="Jonathan Neyra")
        self.policy = Policy.objects.create(
            concept="Gastos medicos menores",
            agent=self.agent,
            holder=self.user,
        )
        self.dependent = Dependent.objects.create(
            name="Estela Nieves",
            policy=self.policy,
        )

    def test_retrive_policies(self):
        client = Client(schema)
        mutation = """
        query {
          policies {
            concept
            holder {
              name
            }
            agent {
              name
            }
            dependents {
              name
            }
          }
        }
        """
        result = client.execute(mutation)
        self.assertTrue(result['data']['policies'])
