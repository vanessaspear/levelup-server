from django.db import models

class Game(models.Model):

    title = models.CharField(max_length=50)
    minimum_players = models.IntegerField(default=2)
    maximum_players = models.IntegerField()
    maker = models.CharField(max_length=50)
    skill_level = models.IntegerField()
    gamer = models.ForeignKey("Gamer", null=True, blank=True, on_delete=models.SET_NULL, related_name='games_created')
    type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name='games')
