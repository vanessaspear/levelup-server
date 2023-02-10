from django.db import models

class Event(models.Model):

    title = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    address = models.CharField(max_length=155)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='game_events')
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='organizer_event')
    attendees = models.ManyToManyField("Gamer", through="Attendee")

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value