from rest_framework import generics,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,AuditLog
from .serializers import UserSerializer,AuditSerializer
class RegisterView(generics.CreateAPIView): queryset=User.objects.all(); serializer_class=UserSerializer; permission_classes=[permissions.AllowAny]
class LoginView(APIView):
 permission_classes=[permissions.AllowAny]
 def post(self,request):
  from django.contrib.auth import authenticate
  email=request.data.get("email"); password=request.data.get("password"); u=authenticate(username=email,password=password)
  if not u: return Response({"detail":"Credenciais inválidas"},status=401)
  r=RefreshToken.for_user(u); AuditLog.objects.create(user_id=u.id,action="login",resource="auth",ip_address=request.META.get("REMOTE_ADDR"))
  return Response({"refresh":str(r),"access":str(r.access_token),"user":UserSerializer(u).data})
class MeView(APIView):
 def get(self,request): return Response(UserSerializer(request.user).data)
class AuditView(generics.ListAPIView):
 queryset=AuditLog.objects.all().order_by("-created_at"); serializer_class=AuditSerializer
 def get_queryset(self):
  if not (self.request.user.is_superuser or self.request.user.role in ["admin","coordinator"]): return AuditLog.objects.none()
  return super().get_queryset()
