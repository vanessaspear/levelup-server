"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game
from rest_framework.decorators import action
from django.db.models import Count, Q
from django.core.exceptions import ValidationError

class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.annotate(
                attendees_count=Count('attendees')).get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message:': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """

        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.annotate(
            attendees_count=Count('attendees'),
            joined=Count(
                'attendees',
                filter=Q(attendees=gamer)
            )
        )

        if "game" in request.query_params: 
            if request.query_params['game'] == '1':
                events = events.filter(game_id=1)
            elif request.query_params['game'] == '2':
                events = events.filter(game_id=2)
        
        # This loop can be removed since the joined property is being set through the annotate on line 38
        # for event in events:
        #     event.joined = gamer in event.attendees.all()

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    # {
    #     "title": "A Sad Event",
    #     "datetime": "2023-02-19T02:30:00Z",
    #     "address": "8675 309",
    #     "type": "Pops"
    # }


    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        game = Game.objects.get(pk=request.data['game'])
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer, game=game)
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
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Leave request for a user to leave an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)

class GamerEventSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Gamer
        fields = ('id', 'bio', 'full_name')

class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'datetime', 'address', 'game']

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    gamer = GamerEventSerializer(many=False)
    attendees_count = serializers.IntegerField(default=None)

    class Meta:
        model = Event
        fields = ('id', 'title', 'datetime', 'address', 'game', 'gamer', 'attendees', 'joined', 'attendees_count')
        depth = 1
