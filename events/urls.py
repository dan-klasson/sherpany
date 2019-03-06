from django.urls import path
from . import views

app_name = 'event'
urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('add', views.EventCreateView.as_view(), name='create'),
    path('edit/<int:pk>', views.EventUpdateView.as_view(), name='update'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='detail'),
    path('attend/<int:pk>', views.AttendanceView.as_view(), name='attend'),
]