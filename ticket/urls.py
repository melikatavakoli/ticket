from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ticket import views

router = DefaultRouter()

router.register('tickets', views.TicketViewSet, basename='ticket')

app_name = 'ticket'
urlpatterns = [
    path('', include(router.urls)),
    path('user-ticket-detail/', views.UserTicketDetailAPIView.as_view(), name='user-ticket-detail'),
    path('user-ticket-reply/<uuid:ticket_id>/', views.UserReplyTicketAPIView.as_view(), name='user-ticket-reply'),
]
