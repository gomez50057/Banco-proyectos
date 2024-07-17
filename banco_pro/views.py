from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
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
from datetime import datetime

from .models import FormProject
from .serializers import FormProjectSerializer
from .utils import siglas, sector_codes
from django.views.generic import TemplateView


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
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def ver_proyectos_tabla(request):
    proyectos = FormProject.objects.filter(estatus__in=['Atendido', 'En Proceso']).values(
        'project_id', 'project_name', 'estatus', 'porcentaje_avance', 'observaciones'
    )
    return JsonResponse(list(proyectos), safe=False)

@login_required
def ver_proyectos_usuario(request):
    user = request.user
    proyectos = FormProject.objects.filter(user=user).values(
        'project_id', 'project_name', 'estatus', 'porcentaje_avance', 'observaciones'
    )
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
    return render(request, 'project_list.html', {'projects': projects})

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
    def get(self, request, project_id=None):
        if project_id:
            project = get_object_or_404(FormProject, project_id=project_id)
            serializer = FormProjectSerializer(project)
            return JsonResponse(serializer.data, safe=False)
        else:
            projects = FormProject.objects.values(
                'id', 'project_id', 'fecha_registro', 'project_name', 'sector', 'tipo_proyecto', 
                'tipo_entidad', 'dependencia', 'organismo', 'municipioEnd', 'peticion_personal', 
                'unidad_responsable', 'unidad_presupuestal', 'ramo_presupuestal', 'monto_federal', 
                'monto_estatal', 'monto_municipal', 'monto_otros', 'inversion_estimada', 'descripcion', 
                'situacion_sin_proyecto', 'objetivos', 'metas', 'gasto_programable', 'programa_presupuestario', 
                'beneficiarios', 'alineacion_normativa', 'region', 'municipio', 'municipio_impacto', 
                'localidad', 'barrio_colonia_ejido', 'latitud', 'longitud', 'plan_nacional', 'plan_estatal', 
                'plan_municipal', 'ods', 'plan_sectorial', 'indicadores_estrategicos', 'indicadores_tacticos', 
                'indicadores_desempeno', 'indicadores_rentabilidad', 'estado_inicial', 'estado_con_proyecto', 
                'estudios_prospectivos', 'estudios_factibilidad', 'analisis_alternativas', 'validacion_normativa',
                'liberacion_derecho_via', 'situacion_sin_proyecto_fotografico', 'situacion_con_proyecto_proyeccion',
                'analisis_costo_beneficio', 'expediente_tecnico', 'proyecto_ejecutivo', 'manifestacion_impacto_ambiental',
                'otros_estudios', 'observaciones', 'porcentaje_avance', 'estatus', 'situacion', 'retroalimentacion',
                'user__username',
                # Campos de bloqueo
                'isBlocked_project_name', 'isBlocked_sector', 'isBlocked_tipo_proyecto', 'isBlocked_tipo_entidad',
                'isBlocked_dependencia', 'isBlocked_organismo', 'isBlocked_municipioEnd', 'isBlocked_peticion_personal',
                'isBlocked_unidad_responsable', 'isBlocked_unidad_presupuestal', 'isBlocked_ramo_presupuestal',
                'isBlocked_monto_federal', 'isBlocked_monto_estatal', 'isBlocked_monto_municipal', 'isBlocked_monto_otros',
                'isBlocked_inversion_estimada', 'isBlocked_descripcion', 'isBlocked_situacion_sin_proyecto', 'isBlocked_objetivos',
                'isBlocked_metas', 'isBlocked_gasto_programable', 'isBlocked_programa_presupuestario', 'isBlocked_beneficiarios',
                'isBlocked_alineacion_normativa', 'isBlocked_region', 'isBlocked_municipio', 'isBlocked_municipio_impacto',
                'isBlocked_localidad', 'isBlocked_barrio_colonia_ejido', 'isBlocked_latitud', 'isBlocked_longitud',
                'isBlocked_plan_nacional', 'isBlocked_plan_estatal', 'isBlocked_plan_municipal', 'isBlocked_ods',
                'isBlocked_plan_sectorial', 'isBlocked_indicadores_estrategicos', 'isBlocked_indicadores_tacticos',
                'isBlocked_indicadores_desempeno', 'isBlocked_indicadores_rentabilidad', 'isBlocked_estado_inicial',
                'isBlocked_estado_con_proyecto', 'isBlocked_estudios_prospectivos', 'isBlocked_estudios_factibilidad',
                'isBlocked_analisis_alternativas', 'isBlocked_validacion_normativa', 'isBlocked_liberacion_derecho_via',
                'isBlocked_situacion_sin_proyecto_fotografico', 'isBlocked_situacion_con_proyecto_proyeccion',
                'isBlocked_analisis_costo_beneficio', 'isBlocked_expediente_tecnico', 'isBlocked_proyecto_ejecutivo',
                'isBlocked_manifestacion_impacto_ambiental', 'isBlocked_otros_estudios', 'isBlocked_observaciones',
                'isBlocked_porcentaje_avance', 'isBlocked_estatus', 'isBlocked_situacion', 'isBlocked_retroalimentacion',
                # Campos de observación
                'observacion_project_name', 'observacion_sector', 'observacion_tipo_proyecto', 'observacion_tipo_entidad',
                'observacion_dependencia', 'observacion_organismo', 'observacion_municipioEnd', 'observacion_peticion_personal',
                'observacion_unidad_responsable', 'observacion_unidad_presupuestal', 'observacion_ramo_presupuestal',
                'observacion_monto_federal', 'observacion_monto_estatal', 'observacion_monto_municipal', 'observacion_monto_otros',
                'observacion_inversion_estimada', 'observacion_descripcion', 'observacion_situacion_sin_proyecto', 'observacion_objetivos',
                'observacion_metas', 'observacion_gasto_programable', 'observacion_programa_presupuestario', 'observacion_beneficiarios',
                'observacion_alineacion_normativa', 'observacion_region', 'observacion_municipio', 'observacion_municipio_impacto',
                'observacion_localidad', 'observacion_barrio_colonia_ejido', 'observacion_latitud', 'observacion_longitud',
                'observacion_plan_nacional', 'observacion_plan_estatal', 'observacion_plan_municipal', 'observacion_ods',
                'observacion_plan_sectorial', 'observacion_indicadores_estrategicos', 'observacion_indicadores_tacticos',
                'observacion_indicadores_desempeno', 'observacion_indicadores_rentabilidad', 'observacion_estado_inicial',
                'observacion_estado_con_proyecto', 'observacion_estudios_prospectivos', 'observacion_estudios_factibilidad',
                'observacion_analisis_alternativas', 'observacion_validacion_normativa', 'observacion_liberacion_derecho_via',
                'observacion_situacion_sin_proyecto_fotografico', 'observacion_situacion_con_proyecto_proyeccion',
                'observacion_analisis_costo_beneficio', 'observacion_expediente_tecnico', 'observacion_proyecto_ejecutivo',
                'observacion_manifestacion_impacto_ambiental', 'observacion_otros_estudios', 'observacion_observaciones',
                'observacion_porcentaje_avance', 'observacion_estatus', 'observacion_situacion', 'observacion_retroalimentacion'
            )
            return JsonResponse(list(projects), safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            data['user'] = request.user.id  # Agregar el usuario actual al proyecto
            serializer = FormProjectSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'Project created successfully', 'project_name': serializer.data['project_name']})
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, project_id):
        try:
            project = get_object_or_404(FormProject, project_id=project_id)
            data = json.loads(request.body)
            for key, value in data.items():
                # Asegurarse de que los campos bloqueados no se actualicen
                if not getattr(project, f'isBlocked_{key}', False):
                    setattr(project, key, value)
            project.save()
            return JsonResponse({'message': 'Project updated successfully'})
        except FormProject.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, project_id):
        try:
            project = get_object_or_404(FormProject, project_id=project_id)
            project.delete()
            return JsonResponse({'message': 'Project deleted successfully'})
        except FormProject.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)

def generate_project_id(entity_type, entity_name, sector, current_year):
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

    data['user'] = request.user.id  # Añadir el ID del usuario autenticado
    serializer = FormProjectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReactAppView(TemplateView):
    template_name = "index.html"