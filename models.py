from tortoise.models import Model
from tortoise import fields

class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    tournament = fields.ForeignKeyField('models.Tournament', related_name='events')
    participants = fields.ManyToManyField('models.Team', related_name='events', through='event_team')

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    def __str__(self):
        return self.name