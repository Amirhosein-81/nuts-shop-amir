from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework import viewsets, permissions
from .serializers import RegisterSerializer
from .models import User,Address
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from .serializers import ChangePasswordSerializer,LogoutSerializer,CustomTokenObtainPairSerializer,UserProfileSerializer,AddressSerializer





class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class UpdateUserProfileView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # تغییر رمز
        new_password = serializer.validated_data["new_password"]
        request.user.set_password(new_password)
        request.user.save()

        return Response({"detail": "رمز عبور با موفقیت تغییر کرد."}, status=200)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "با موفقیت خارج شدید."}, status=200)


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # فقط آدرس‌های کاربر لاگین‌شده
        return Address.objects.filter(user=self.request.user)