from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from config.throttles import (
    ForgotPasswordThrottle,
    LoginThrottle,
    RegisterThrottle,
    ResendVerificationThrottle,
)

from .permissions import IsAdmin
from .services import AuthService


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([RegisterThrottle])
def register_view(request):
    data = AuthService.register(request.data)
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([LoginThrottle])
def login_view(request):
    data = AuthService.login(request.data)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response(
            {'error': 'El refresh token es obligatorio.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    AuthService.logout(refresh_token)
    return Response(status=status.HTTP_205_RESET_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_view(request):
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response(
            {'error': 'El refresh token es obligatorio.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    data = AuthService.refresh(refresh_token)
    if data is None:
        return Response(
            {'error': 'Refresh token inválido o expirado.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ForgotPasswordThrottle])
def forgot_password_view(request):
    data = AuthService.forgot_password(request.data)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    AuthService.change_password(request.user, request.data)
    return Response(
        {'message': 'Contraseña actualizada exitosamente.'},
        status=status.HTTP_200_OK,
    )


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    if request.method == 'GET':
        data = AuthService.get_profile(request.user)
        return Response(data, status=status.HTTP_200_OK)

    data = AuthService.update_profile(request.user, request.data)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_view(request):
    try:
        data = AuthService.reset_password(request.data)
        return Response(data, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_view(request):
    try:
        data = AuthService.verify_email(request.data)
        return Response(data, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([ResendVerificationThrottle])
def resend_verification_view(request):
    data = AuthService.resend_verification(request.data)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def user_list_view(request):
    data = AuthService.list_users(request)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdmin])
def user_detail_view(request, user_id):
    if request.method == 'GET':
        try:
            data = AuthService.get_user_detail(user_id)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        try:
            data = AuthService.update_user(user_id, request.data)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            AuthService.delete_user(user_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
