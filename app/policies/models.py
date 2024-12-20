from django.db import models


class Agent(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Policy(models.Model):
    concept = models.CharField(max_length=500)
    holder = models.ForeignKey(User, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.concept} - {self.holder.name}'


class Dependent(models.Model):
    name = models.CharField(max_length=255)
    policy = models.ForeignKey(
        Policy,
        related_name='dependents',
        on_delete=models.CASCADE
    )
