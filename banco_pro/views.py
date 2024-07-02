# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json

from .models import FormProject
from .serializers import FormProjectSerializer

from datetime import datetime
from django.db.models import Max

@csrf_exempt
def inicio_sesion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            group = user.groups.first().name if user.groups.exists() else 'sin grupo'
            return JsonResponse({'status': 'ok', 'group': group})
        else:
            return JsonResponse({'status': 'error', 'message': 'Credenciales inválidas'}, status=400)

# @api_view(['POST'])
# def create_project(request):
#     serializer = FormProjectSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def ver_proyectos_tabla(request):
    proyectos = FormProject.objects.values('project_name', 'descripcion', 'tipo_proyecto', 'municipio', 'beneficiarios')
    return JsonResponse(list(proyectos), safe=False)

class BulkCreateProjects(APIView):
    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({"error": "Se esperaba una lista de objetos"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = FormProjectSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@staff_member_required
def project_list_view(request):
    projects = FormProject.objects.all()
    return render(request, {'projects': projects})

@login_required
def current_user(request):
    user = request.user
    user_data = {
        'username': user.username,
        'email': user.email,
        'groups': list(user.groups.values_list('name', flat=True)),
    }
    return JsonResponse(user_data)

def redirect_to_home(request):
    return redirect('/')

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
            return JsonResponse({'message': 'Project created successfully', 'project_name': project.project_name})
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






from datetime import datetime
from .models import FormProject
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import FormProjectSerializer
from .utils import siglas, sector_codes

def generate_project_id(entity_type, entity_name, sector, current_year):
    # Ajustar para obtener correctamente la sigla
    entity_sigla = siglas.get(entity_type, {}).get(entity_name, 'UNK')
    
    if entity_sigla == 'UNK':
        print(f"Sigla no encontrada para el tipo de entidad: {entity_type} y nombre: {entity_name}")

    sector_code = sector_codes.get(sector, 'XX')
    if sector_code == 'XX':
        print(f"Código de sector no proporcionado o inválido: {sector}")

    year = str(current_year)
    consecutive_number = FormProject.objects.filter(fecha_registro__year=current_year).count() + 1
    consecutive_number = str(consecutive_number).zfill(3)

    project_id = f"{entity_sigla}{sector_code}{year}{consecutive_number}"
    print(f"Generado project_id: {project_id}")

    return project_id

@api_view(['POST'])
def create_project(request):
    current_year = datetime.now().year
    data = request.data.copy()
    entity_type = data.get('tipo_entidad')
    entity_name = data.get('dependencia') if entity_type == 'Dependencia' else data.get('organismo') if entity_type == 'Organismo' else data.get('municipioEnd')
    sector = data.get('sector')

    if not entity_type or not entity_name or not sector:
        return Response({'error': 'Faltan datos necesarios para generar el ID del proyecto.'}, status=status.HTTP_400_BAD_REQUEST)

    project_id = generate_project_id(entity_type, entity_name, sector, current_year)
    data['project_id'] = project_id

    serializer = FormProjectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
