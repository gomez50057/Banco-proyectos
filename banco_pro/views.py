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


from django.http import JsonResponse
from django.views import View
from .models import FormProject
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


from django.contrib.auth.decorators import login_required, user_passes_test
from .middleware import admin_required

@method_decorator(admin_required, name='dispatch')
class ProjectView(View):
    def get(self, request):
        projects = FormProject.objects.values(
            'id', 'fecha_registro', 'project_name', 'sector', 'tipo_proyecto', 'tipo_entidad',
            'dependencia', 'organismo', 'municipioEnd', 'peticion_personal', 'unidad_responsable',
            'unidad_presupuestal', 'ramo_presupuestal', 'monto_federal', 'monto_estatal',
            'monto_municipal', 'monto_otros', 'inversion_estimada', 'descripcion',
            'situacion_sin_proyecto', 'objetivos', 'metas', 'gasto_programable',
            'programa_presupuestario', 'beneficiarios', 'alineacion_normativa', 'region',
            'municipio', 'municipio_impacto', 'localidad', 'barrio_colonia_ejido', 'latitud',
            'longitud', 'plan_nacional', 'plan_estatal', 'plan_municipal', 'ods', 'plan_sectorial',
            'indicadores_estrategicos', 'indicadores_tacticos', 'indicadores_desempeno',
            'indicadores_rentabilidad', 'estado_inicial', 'estado_con_proyecto', 'estudios_prospectivos',
            'estudios_factibilidad', 'analisis_alternativas', 'validacion_normativa',
            'liberacion_derecho_via', 'situacion_sin_proyecto_fotografico', 'situacion_con_proyecto_proyeccion',
            'analisis_costo_beneficio', 'expediente_tecnico', 'proyecto_ejecutivo',
            'manifestacion_impacto_ambiental', 'otros_estudios', 'observaciones'
        )
        return JsonResponse(list(projects), safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            project = FormProject.objects.create(**data)
            return JsonResponse({'message': 'Project created successfully', 'project': project.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, pk):
        try:
            project = FormProject.objects.get(pk=pk)
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(project, key, value)
            project.save()
            return JsonResponse({'message': 'Project updated successfully'})
        except FormProject.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, pk):
        try:
            project = FormProject.objects.get(pk=pk)
            project.delete()
            return JsonResponse({'message': 'Project deleted successfully'})
        except FormProject.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)


# Archivo: myapp/views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views import View
from .models import FormProject
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@login_required
def current_user(request):
    user = request.user
    user_data = {
        'username': user.username,
        'email': user.email,
        'groups': list(user.groups.values_list('name', flat=True)),
    }
    return JsonResponse(user_data)

@method_decorator(csrf_exempt, name='dispatch')
class ProjectView(View):
    def get(self, request):
        projects = FormProject.objects.values(
            'id', 'fecha_registro', 'project_name', 'sector', 'tipo_proyecto', 
            'tipo_entidad', 'dependencia', 'organismo', 'municipioEnd', 
            'peticion_personal', 'unidad_responsable', 'unidad_presupuestal', 
            'ramo_presupuestal', 'monto_federal', 'monto_estatal', 'monto_municipal', 
            'monto_otros', 'inversion_estimada', 'descripcion', 'situacion_sin_proyecto', 
            'objetivos', 'metas', 'gasto_programable', 'programa_presupuestario', 
            'beneficiarios', 'alineacion_normativa', 'region', 'municipio', 
            'municipio_impacto', 'localidad', 'barrio_colonia_ejido', 'latitud', 
            'longitud', 'plan_nacional', 'plan_estatal', 'plan_municipal', 'ods', 
            'plan_sectorial', 'indicadores_estrategicos', 'indicadores_tacticos', 
            'indicadores_desempeno', 'indicadores_rentabilidad', 'estado_inicial', 
            'estado_con_proyecto', 'estudios_prospectivos', 'estudios_factibilidad', 
            'analisis_alternativas', 'validacion_normativa', 'liberacion_derecho_via', 
            'situacion_sin_proyecto_fotografico', 'situacion_con_proyecto_proyeccion', 
            'analisis_costo_beneficio', 'expediente_tecnico', 'proyecto_ejecutivo', 
            'manifestacion_impacto_ambiental', 'otros_estudios', 'observaciones'
        )
        return JsonResponse(list(projects), safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            project = FormProject.objects.create(**data)
            return JsonResponse({'message': 'Project created successfully', 'project': project.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, pk):
        try:
            project = FormProject.objects.get(pk=pk)
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(project, key, value)
            project.save()
            return JsonResponse({'message': 'Project updated successfully'})
        except FormProject.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, pk):
        try:
            project = FormProject.objects.get(pk=pk)
            project.delete()
            return JsonResponse({'message': 'Project deleted successfully'})
        except FormProject.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
