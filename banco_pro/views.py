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

@api_view(['POST'])
def create_project(request):
    serializer = FormProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from .models import FormProject

def ver_proyectos_tabla(request):
    proyectos = FormProject.objects.values('project_name', 'descripcion', 'tipo_proyecto', 'municipio', 'beneficiarios')
    return JsonResponse(list(proyectos), safe=False)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FormProject
from .serializers import FormProjectSerializer

class BulkCreateProjects(APIView):
    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({"error": "Se esperaba una lista de objetos"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = FormProjectSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import FormProject

@staff_member_required
def project_list_view(request):
    projects = FormProject.objects.all()
    return render(request, {'projects': projects})
