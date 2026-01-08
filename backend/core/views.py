from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer, UserInviteSerializer
from .permissions import IsFirmAdmin, IsManager
from django.utils.crypto import get_random_string


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
class UserInviteView(APIView):
    permission_classes = [IsAuthenticated, IsFirmAdmin | IsManager]

    def post(self, request):
        serializer = UserInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # <-- FIXED LINE
        password = get_random_string(length=12)  # 12-character random password

        user = User.objects.create(
            email=serializer.validated_data["email"],
            role=serializer.validated_data["role"],
            organization=request.user.organization
        )
        user.set_password(password)
        user.save()

        # Mock email sending
        print(f"INVITE: {user.email} | password: {password}")

        return Response(
            {"message": "User invited successfully"},
            status=status.HTTP_201_CREATED
        )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Only allow user to view their own profile
        if str(request.user.id) != str(id):
            return Response({"detail": "Forbidden"}, status=403)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request, id):
        # Only allow user to update their own profile
        if str(request.user.id) != str(id):
            return Response({"detail": "Forbidden"}, status=403)

        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)