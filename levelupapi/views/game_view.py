"""View module for handling requests about games"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType, Event
from django.db.models import Count, Q
from django.core.exceptions import ValidationError


class GameView(ViewSet):
    """Level up game view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single a game

        Returns:
            Response -- JSON serialized game object
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message:': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        games = Game.objects.annotate(
            event_count=Count('game_events'),
            user_event_count=Count('game_events',
                filter=Q(game_events__gamer=gamer)
            )
        )

        if "type" in request.query_params:
            game_types = GameType.objects.all()

            for iterator in game_types:
                if iterator.id == int(request.query_params['type']):
                    games = games.filter(type_id=iterator.id)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        type = GameType.objects.get(pk=request.data["type"])
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer, type=type)
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

class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['title', 'minimum_players', 'maximum_players', 'maker', 'skill_level', 'type'] 
        
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    event_count = serializers.IntegerField(default=None)
    user_event_count = serializers.IntegerField(default=None)

    class Meta:
        model = Game
        fields = ('id', 'title', 'minimum_players', 'maximum_players', 'maker', 'skill_level', 'gamer_id', 'type', 'event_count', 'user_event_count')
        depth = 1