# views.py

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ProyectoDependencia, Project
from .serializers import UsuarioSerializer, UserSerializer, ProyectoDependenciaSerializer, ProjectSerializer


@api_view(['POST'])
def registro_usuario(request):
    """
    Registra un nuevo usuario.
    """
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        tipo_cuenta = serializer.validated_data.get('tipo_cuenta')

        if User.objects.filter(username=username).exists():
            return Response({"error": "El nombre de usuario ya está en uso"}, status=status.HTTP_400_BAD_REQUEST)
        
        usuario = User.objects.create_user(
            username=username,
            password=serializer.validated_data.get('password'),
        )
        usuario.perfil.tipo_cuenta = tipo_cuenta
        usuario.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def inicio_sesion(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # Si la autenticación es exitosa, devolver un mensaje de éxito
        return Response({"mensaje": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)
    else:
        # Si la autenticación falla, devolver un error
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ver_usuarios_registrados(request):
    """
    Vista para ver todos los usuarios registrados en la base de datos.
    """
    usuarios = User.objects.all()
    serializer = UserSerializer(usuarios, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def guardar_proyecto(request):
    """
    Guarda un nuevo proyecto de dependencia.
    """
    if request.method == 'POST':
        projectName = request.data.get('projectName')
        description = request.data.get('description')
        file = request.FILES.get('file')

        try:
            proyecto = ProyectoDependencia.objects.create(
                projectName=projectName,
                description=description,
                file=file
            )
            serializer = ProyectoDependenciaSerializer(proyecto)
            return JsonResponse(serializer.data, status=201)
        except Exception as e:
            print(f"Error al guardar el proyecto: {e}")
            return JsonResponse({'error': 'Ocurrió un error al guardar el proyecto'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@api_view(['GET'])
def ver_proyectos_registrados(request):
    """
    Vista para ver todos los proyectos registrados.
    """
    proyectos = ProyectoDependencia.objects.all()
    serializer = ProyectoDependenciaSerializer(proyectos, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def ver_proyectos_en_tabla(request):
    """
    Vista para ver todos los proyectos en formato de tabla.
    """
    proyectos = ProyectoDependencia.objects.all()
    serializer = ProyectoDependenciaSerializer(proyectos, many=True)
    data = serializer.data

    table_data = [
        {
            'Project Name': proyecto.get('projectName'),
            'Description': proyecto.get('description'),
            'File': proyecto.get('file')
        }
        for proyecto in data
    ]

    return JsonResponse(table_data, safe=False)


@api_view(['POST'])
def create_project(request):
    """
    Crea un nuevo proyecto.
    """
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
