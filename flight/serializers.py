from rest_framework import serializers
from .models import Flight, Passenger, Reservation

class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = (
            "flight_number",
            "operating_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd"
        )

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"

class ReservationSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer(many = True, required=True)
    flight = serializers.StringRelatedField()
    flight_id = serializers.IntegerField(write_only=True)
    #! write_only 👉 It will only appear when creating
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "flight",  # GET
            "flight_id",  # POST
            "user",  # GET
            "user_id",  # POST
            "passenger"
        )

    def create(self, validated_data):
        passenger_data = validated_data.pop('passenger')
        validated_data['user_id'] = self.context['request'].user.id
        # We updated the user information inside data 👆
        reservation = Reservation.objects.create(**validated_data)
        for passenger in passenger_data:
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)
        reservation.save()
        return reservation

class StaffFlightSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(many=True, read_only=True)
    class Meta:
        model = Flight
        fields = "__all__"
