from django.utils.crypto import get_random_string
from rest_framework import serializers

from services.models import Order
from services.models import Service
from users.serializers import UserModelSerializer


class ServiceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            'id', 'name', 'description', 'price', 'currency', 'is_available',
        )


class OrderModelSerializer(serializers.ModelSerializer):
    assigned_staff = serializers.SerializerMethodField()
    ordered_service = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'title', 'number', 'status', 'service', 'notes', 'customer_first_name',
            'customer_last_name', 'customer_phone', 'assigned_staff', 'ordered_service',
            'is_phone_verified',
        )
        read_only_fields = ('number',)

    @staticmethod
    def get_assigned_staff(order):
        return UserModelSerializer(order.user).data

    @staticmethod
    def get_ordered_service(order):
        return ServiceModelSerializer(order.service).data

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        verification_code = get_random_string(5).upper()
        order.user.send_sms(
            body='Verification code: {}'.format(verification_code),
            sms_to=order.customer_phone
        )
        order.phone_verification_code = verification_code
        order.save(update_fields=['phone_verification_code'])
        return order


class OrderConfirmModelSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'status', 'verification_code',
        )
