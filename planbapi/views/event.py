from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from planbapi.models import *


class EventViewSet(ViewSet):
    def list(self, request):
        """Handle GET requests to events resource
        Returns:
            Response -- JSON serialized list of events
        """
        # Get the current authenticated user
        customer = Customer.objects.get(user=request.auth.user)
        events = Event.objects.filter(customer=customer).order_by('date')

        # Support filtering events by user
        current_user = self.request.query_params.get('customer', None)
        if current_user is not None:
            events = events.filter(user=customer)

        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event
        Returns:
            Response -- JSON serialized event instance
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized event instance
        """

        # Uses the token passed in the `Authorization` header
        customer = Customer.objects.get(user=request.auth.user)

        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.
        event = Event()
        event.customer = customer
        event.name = request.data["name"]
        event.date = request.data["date"]
        event.budget = request.data["budget"]

        try:
            event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single event
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)

        event.name = request.data["name"]
        event.date = request.data["date"]
        event.budget = request.data["budget"]

        try:
            event.save()
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True)
    @csrf_exempt
    def product(self, request, pk=None):
        if request.method == "POST":
            event = Event.objects.get(pk=pk)
            product = Product.objects.get(pk=request.data['productId'])

            try:
                adding = EventProduct.objects.get(
                    event=event, product=product
                )
                return Response(
                    {'message': 'Event already used this product.'},
                    status=status.HTTP_204_NO_CONTENT
                )
            except EventProduct.DoesNotExist:
                adding = EventProduct()
                adding.event = event
                adding.product = product
                adding.save()

                return Response({}, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            try:
                event = Event.objects.get(pk=pk)
            except Event.DoesNotExist:
                return Response(
                    {'message': 'Event does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            product = Product.objects.get(pk=request.data['productId'])

            try:
                reacting = EventProduct.objects.get(
                    event=event, product=product
                )
                reacting.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except EventProduct.DoesNotExist:
                return Response(
                    {'message': 'User has not used this product.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'budget', 'customer', 'products')
        depth = 1
