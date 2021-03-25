from django.urls import path, include

from authorization.views import registration

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', registration, name='registration'),

]
