from django.db import models

class Attendee(models.Model):

    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='registered_gamers')
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='event_registrations')