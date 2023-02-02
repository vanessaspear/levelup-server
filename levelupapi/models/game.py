from django.db import models

class Game(models.Model):

    title = models.CharField(max_length=50)
    num_players = models.IntegerField(min_value=2)
    maker = models.CharField(max_length=50)
    skill_level = models.IntegerField(min_value=0, max_value=10)
    gamer = models.ForeignKey("Gamer", null=True, blank=True, on_delete=models.SET_NULL, related_name='games_created')
    type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name='games')
