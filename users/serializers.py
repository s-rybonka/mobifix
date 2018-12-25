from rest_framework import serializers
from users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id', 'first_name', 'last_name', 'address', 'phone',
            'facebook', 'twitter',
        )
