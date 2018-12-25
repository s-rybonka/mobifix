"""mobifix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="MOBIFIX API",
        default_version='v1',
        description="Private API for interactions with server in REST style.",
        terms_of_service="https://example.com/terms",
        contact=openapi.Contact(email="stanislav.rybonka@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^$', lambda request: redirect('api:docs')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include([
        url(r'^auth/', include("auth.urls", namespace='auth')),
        url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
    ],
        namespace='api',
    ))
]
