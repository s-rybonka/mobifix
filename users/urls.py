from django.conf.urls import url
from users import api as api_views

urlpatterns = [
    url(r'^profile/', api_views.ProfileRetrieveUpdateAPIView.as_view(), name='profile'),
]