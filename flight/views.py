from django.shortcuts import render
from .serializers import FlightSerializer
from rest_framework import viewsets
from .models import Flight, Passenger, Reservation
from .permissions import IsStafforReadOnly
#! Thanks to the ModelViewSet, we can do all the operations 👇
#!  GET, POST, PUT, DELETE, PATCH
class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStafforReadOnly,)