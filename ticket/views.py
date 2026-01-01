from django.db.models import Q
from rest_framework import filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from common.paginations import CustomLimitOffsetPagination
from ticket.models import Ticket, TicketDetail
from rest_framework import generics
from ticket.serializers import TicketDetailSerializer, UserCreateTicketSerializer,\
    UserReplyTicketSerializer, UserTicketListSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
# from ticket.ticket_export import export_ticket_data
User = get_user_model()

# # ========================================================================================
# # ================== Ticket Export APIView
# # ========================================================================================-
# class TicketExportAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         ticket_id = request.query_params.get("ticket_id")

#         serializer = TicketExportInputSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         fields = serializer.validated_data.get("fields")

#         data = export_ticket_data(
#             ticket_id=ticket_id,
#             selected_fields=fields
#         )

#         return Response(
#             {
#                 "ticket_id": ticket_id,
#                 "count": len(data),
#                 "data": data,
#             },
#             status=status.HTTP_200_OK
#         )

# # ========================================================================================
# # ================== IsUserOrAdminStaff
# # ========================================================================================-
class IsUserOrAdminStaff(permissions.BasePermission):
    """
    - admin (base_role=admin) همیشه مجاز
    - user فقط اگر Staff معتبر داشته باشد
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if str(request.user.base_role).lower() == 'admin':
            return True
        if str(request.user.base_role).lower() == 'user':
            staff = request.user.user_staff.first()
            if not staff:
                return False

            return (
                staff.is_present and
                staff.role and
                staff.role.key in ['user', 'admin']
            )

        return False
    
# # ========================================================================================
# # ================== User Ticket Detail APIView
# # ========================================================================================-
class UserTicketDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ticket_id = request.GET.get('ticket_id')
        if not ticket_id:
            return Response({'detail': 'ticket_id required'}, status=400)

        ticket = Ticket.objects.filter(id=ticket_id, user=request.user).first()
        if not ticket:
            return Response({'detail': 'تیکت یافت نشد'}, status=404)

        data = {
            'title': ticket.title,
            'number': ticket.number,
            'priority': ticket.priority,
            'is_active': ticket.is_active,
            'status': ticket.get_status_display(),
            'details': TicketDetailSerializer(ticket.ticket.all(), many=True).data
        }
        return Response(data)
    
# # ========================================================================================
# # ================== Ticket ViewSet
# # ========================================================================================-
class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsUserOrAdminStaff()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserTicketListSerializer
        if self.action == 'create':
            return UserCreateTicketSerializer
        return UserTicketListSerializer

# # ========================================================================================
# # ================== User Reply Ticket APIView
# # ========================================================================================-
class UserReplyTicketAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id):
        ticket = Ticket.objects.filter(id=ticket_id, user=request.user).first()
        if not ticket:
            return Response({'detail': 'تیکت یافت نشد'}, status=404)

        serializer = UserReplyTicketSerializer(
            data=request.data,
            context={'request': request, 'ticket': ticket}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'پاسخ ثبت شد'}, status=201)