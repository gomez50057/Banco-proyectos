from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import FormProject
from .serializers import UserSerializer, FormProjectSerializer

# @api_view(['POST'])
# def registro_usuario(request):
#     serializer = UsuarioSerializer(data=request.data)
#     if serializer.is_valid():
#         username = serializer.validated_data.get('username')
#         tipo_cuenta = serializer.validated_data.get('tipo_cuenta')

#         if User.objects.filter(username=username).exists():
#             return Response({"error": "El nombre de usuario ya está en uso"}, status=status.HTTP_400_BAD_REQUEST)
        
#         usuario = User.objects.create_user(
#             username=username,
#             password=serializer.validated_data.get('password'),
#         )
#         usuario.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def inicio_sesion(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        return Response({"mensaje": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ver_usuarios_registrados(request):
    usuarios = User.objects.all()
    serializer = UserSerializer(usuarios, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_project(request):
    serializer = FormProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
