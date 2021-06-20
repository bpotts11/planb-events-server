# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from django.http import HttpResponseServerError
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import serializers
# from planbapi.models import *


# class EventViewSet(ViewSet):

#     def list(self, request):
#         events = Event.objects.all().order_by('date')

#         current_user = self.request.query_params.get('user', None)
#         if current_user is not None:
#             events = events.filter(user=planb_customer)

#         serializer = EventSerializer(
#             events, many=True, context={'request': request})
#         return Response(serializer.data)

#     # def list(self, request):
#     #     """Handle GET requests to events resource
#     #     Returns:
#     #         Response -- JSON serialized list of events
#     #     """
#     #     # Get the current authenticated user
#     #     planb_customer = Customer.objects.get(user=request.auth.user)
#     #     events = Event.objects.order_by('date')

#     #     # Support filtering posts by user
#     #     current_user = self.request.query_params.get('customer', None)
#     #     if current_user is not None:
#     #         events = events.filter(user=planb_customer)

#     #     serializer = EventSerializer(
#     #         events, many=True, context={'request': request})
#     #     return Response(serializer.data)


# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = ('id', 'name', 'date', 'budget', 'customer')
