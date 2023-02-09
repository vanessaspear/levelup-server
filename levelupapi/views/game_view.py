"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """Level up game view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single a game

        Returns:
            Response -- JSON serialized game object
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        game = Game.objects.all()
        serializer = GameSerializer(game, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        type = GameType.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            maximum_players=request.data["maximum_players"],
            minimum_players=request.data["minimum_players"],
            skill_level=request.data["skill_level"],
            gamer=gamer,
            type=type
        )
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handles PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.maximum_players=request.data["maximum_players"]
        game.minimum_players=request.data["minimum_players"]
        game.skill_level = request.data["skill_level"]

        game_type = GameType.objects.get(pk=request.data["game_type"])
        game.type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Game
        fields = ('id', 'title', 'minimum_players', 'maximum_players', 'maker', 'skill_level', 'gamer_id', 'type')
