from rest_framework import serializers

from users.models import Profile
from users.models import User


class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id', 'first_name', 'last_name', 'address', 'phone',
            'facebook', 'twitter',
        )


class UserModelSerializer(serializers.ModelSerializer):
    profile = ProfileModelSerializer()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'type', 'profile',
        )
