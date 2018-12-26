from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import Profile
from users.serializers import ProfileModelSerializer


class ProfileRetrieveUpdateAPIView(UpdateAPIView, RetrieveAPIView):
    serializer_class = ProfileModelSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            pk=self.request.user.profile.id
        )
