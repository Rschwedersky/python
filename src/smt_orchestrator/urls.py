from django.urls import path

from . import views

urlpatterns = [
    path('api/v1/get_schedule_state/<str:id>',
         views.get_state, name='get_schedule_state'),
]
