from django.shortcuts import render
from requests import request
from .serializers import FlightSerializer, ReservationSerializer, StaffFlightSerializer
from rest_framework import viewsets
from .models import Flight, Passenger, Reservation
from .permissions import IsStafforReadOnly
from datetime import datetime, date

#! Thanks to the ModelViewSet, we can do all the operations 👇
#!  GET, POST, PUT, DELETE, PATCH
class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStafforReadOnly,)

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.request.user.is_staff:
            return StaffFlightSerializer
        return serializer

    def get_queryset(self):
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        today = date.today()

        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            queryset = Flight.objects.filter(date_of_departure__gt = today)
            if Flight.objects.filter(date_of_departure = today):
                today_qs = Flight.objects.filter(date_of_departure = today).filter(etd__gt=current_time)
            queryset = queryset.union(today_qs)
            return queryset

class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    #! Overriding "get_queryset" Method 👇
    def get_queryset(self):
        queryset = super().get_queryset() # 👉 Reservation.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user = self.request.user)