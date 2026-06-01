from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import DashboardService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    data = DashboardService.get_user_stats(request.user)
    return Response(data, status=status.HTTP_200_OK)
