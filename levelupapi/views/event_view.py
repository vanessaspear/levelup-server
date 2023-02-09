"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game

class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """

        events = Event.objects.all()

        if "game" in request.query_params: 
            if request.query_params['game'] == '1':
                events = events.filter(game_id=1)
            elif request.query_params['game'] == '2':
                events = events.filter(game_id=2)
        
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        game = Game.objects.get(pk=request.data['game'])
        gamer = Gamer.objects.get(user=request.auth.user)

        new_event = Event.objects.create(
            title=request.data['title'],
            datetime=request.data['datetime'],
            address=request.data['address'],
            game=game,
            gamer=gamer
        )

        serializer = EventSerializer(new_event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handles PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.title = request.data["title"]
        event.datetime = request.data["datetime"]
        event.address = request.data["address"]

        game = Game.objects.get(pk=request.data['game'])
        event.game = game
        gamer = Gamer.objects.get(user=request.auth.user)
        event.gamer = gamer
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class GamerEventSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Gamer
        fields = ('id', 'bio', 'full_name')

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    gamer = GamerEventSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'title', 'datetime', 'address', 'game', 'gamer')
        depth = 1
