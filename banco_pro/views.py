from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UsuarioSerializer

from django.shortcuts import render
from django.http import JsonResponse
from .models import ProyectoDependencia 
from .serializers import UserSerializer




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
        else:
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
    """
    Inicia sesión con el nombre de usuario proporcionado.
    """
    username = request.data.get('username')

    if User.objects.filter(username=username).exists():
        return Response({"mensaje": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ver_usuarios_registrados(request):
    """
    Vista para ver todos los usuarios registrados en la base de datos.
    """
    # Obtener todos los usuarios registrados
    usuarios = User.objects.all()
    # Serializar los usuarios
    serializer = UserSerializer(usuarios, many=True)
    # Devolver la lista de usuarios serializados como una respuesta JSON
    return Response(serializer.data)


# Guardado del proyecto formulario 


from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import ProyectoDependencia 
from .serializers import ProyectoDependenciaSerializer

@api_view(['POST'])
def guardar_proyecto(request):
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
    proyectos = ProyectoDependencia.objects.all()
    serializer = ProyectoDependenciaSerializer(proyectos, many=True)
    return JsonResponse(serializer.data, safe=False)


from django.http import JsonResponse
from .models import ProyectoDependencia
from .serializers import ProyectoDependenciaSerializer





def ver_proyectos_en_tabla(request):
    proyectos = ProyectoDependencia.objects.all()
    serializer = ProyectoDependenciaSerializer(proyectos, many=True)
    data = serializer.data

    # Formatear los datos de la tabla
    table_data = []
    for proyecto in data:
        table_data.append({
            'Project Name': proyecto.get('projectName'),
            'Description': proyecto.get('description'),
            'File': proyecto.get('file')
        })

    return JsonResponse(table_data, safe=False)
