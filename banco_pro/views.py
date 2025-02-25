import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sessions.models import Session
from django.db.models import Count, F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FormProject, AnexoProyecto, CedulaRegistro
from .serializers import (
    FormProjectSerializer,
    BulkCreateProjectSerializer,
    CedulaRegistroSerializer,
    AnexoProyectoSerializer,
)
from .utils import siglas, sector_codes, generate_proj_investment_id


from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import FormProject, Document
from .serializers import DocumentSerializer

# from .models import FormProjectHistory

@csrf_exempt
def inicio_sesion(request):
    """
    Vista para el inicio de sesión del usuario.
    
    Método POST:
      - Recibe un JSON con 'username' y 'password'.
      - Autentica al usuario y, de ser exitoso, inicia la sesión.
      - Retorna el nombre del grupo del usuario (o 'sin grupo' si no pertenece a ninguno).
    
    Otros métodos:
      - Retorna error indicando que el método no está permitido.
    """
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


@method_decorator(csrf_exempt, name='dispatch')
class BulkCreateUsers(View):
    """
    Vista para la creación masiva de usuarios.
    
    Método POST:
      - Recibe una lista de objetos JSON con los datos de los usuarios.
      - Valida que se incluyan 'username', 'password' y 'tipo_cuenta'.
      - Crea el usuario y lo añade al grupo correspondiente.
      - Retorna un listado de los nombres de usuarios creados.
    """
    def post(self, request):
        try:
            # Lee el cuerpo de la solicitud y lo convierte en objeto JSON
            data = json.loads(request.body)
            
            # Verifica que data sea una lista de usuarios
            if not isinstance(data, list):
                return JsonResponse({"error": "Se esperaba una lista de objetos"}, status=400)
            
            created_users = []
            for user_data in data:
                username = user_data.get('username')
                password = user_data.get('password')
                tipo_cuenta = user_data.get('tipo_cuenta')

                if not username or not password or not tipo_cuenta:
                    return JsonResponse({"error": "Faltan datos requeridos: 'username', 'password', o 'tipo_cuenta'"}, status=400)

                # Crear el usuario
                user = User.objects.create_user(username=username, password=password)

                # Añadir el usuario al grupo correspondiente
                group, created = Group.objects.get_or_create(name=tipo_cuenta)
                user.groups.add(group)
                user.save()

                created_users.append(user.username)

            return JsonResponse({"message": "Usuarios creados con éxito", "users": created_users}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


def ver_proyectos_tabla(request):
    """
    Vista que retorna una lista de proyectos filtrados por estatus ('Atendido' o 'En Proceso').

    Retorna un JSON con los campos: project_id, nombre_proyecto, estatus, porcentaje_avance y observaciones.
    """
    proyectos = FormProject.objects.filter(estatus__in=['Atendido', 'En Proceso']).values(
        'project_id', 'nombre_proyecto', 'estatus', 'porcentaje_avance', 'observaciones'
    )
    return JsonResponse(list(proyectos), safe=False)

def ver_proyectos_tabla_admin(request):
    """
    Vista que retorna una lista de todos los proyectos, mostrando todos los campos del modelo
    excepto aquellos que comienzan con 'isBlocked' o 'observacion',
    y reemplazando el campo 'user' por el nombre de usuario.
    """
    proyectos = FormProject.objects.all().select_related('user')
    resultado = []
    
    for proyecto in proyectos:
        datos = {}
        for field in proyecto._meta.fields:
            field_name = field.name
            # Excluir campos que comienzan con 'isBlocked' o 'observacion'
            if field_name.startswith('isBlocked') or field_name.startswith('observacion'):
                continue
            # Si es el campo 'user', se reemplaza por el nombre de usuario
            if field_name == 'user':
                datos[field_name] = proyecto.user.username
            else:
                datos[field_name] = getattr(proyecto, field_name)
        resultado.append(datos)
        
    return JsonResponse(resultado, safe=False)



@login_required
def ver_proyectos_usuario(request):
    """
    Vista que retorna los proyectos asociados al usuario autenticado.

    Retorna un JSON con los campos:
      - isBlocked_project
      - estatus
      - project_id
      - nombre_proyecto
      - porcentaje_avance
      - observaciones
    """
    user = request.user
    proyectos = FormProject.objects.filter(user=user).values(
        'isBlocked_project','estatus' , 'project_id', 'nombre_proyecto', 'estatus', 'porcentaje_avance', 'observaciones'
    )
    return JsonResponse(list(proyectos), safe=False)


class BulkCreateProjects(APIView):
    """
    APIView para la creación masiva de proyectos.
    
    Método POST:
      - Recibe una lista de objetos JSON.
      - Utiliza el serializer BulkCreateProjectSerializer para validar y guardar los proyectos.
      - Retorna los datos de los proyectos creados o errores de validación.
    """
    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({"error": "Se esperaba una lista de objetos"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BulkCreateProjectSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@staff_member_required
def project_list_view(request):
    """
    Vista accesible solo para staff que renderiza una plantilla HTML con la lista completa de proyectos.
    """
    projects = FormProject.objects.all()
    return render(request, 'project_list.html', {'projects': projects})


@login_required
def current_user(request):
    """
    Vista que retorna información básica del usuario autenticado.

    Retorna un JSON con los campos:
      - username
      - email
      - groups (lista de nombres de grupo a los que pertenece)
    """
    user = request.user
    user_data = {
        'username': user.username,
        'email': user.email,
        'groups': list(user.groups.values_list('name', flat=True)),
    }
    return JsonResponse(user_data)


def redirect_to_home(request):
    """
    Vista que redirige a la página de inicio.
    """
    return redirect('/')


# Constantes para la obtención de campos y prefijos de bloqueo y observación.
FIELDS_TO_FETCH = ['project_id', 'area_adscripcion', 'user', 'nombre_registrante', 'apellido_paterno', 'apellido_materno', 'correo', 'telefono', 'telefono_ext', 'fecha_registro', 'nombre_proyecto', 'sector', 'tipo_proyecto', 'tipo_entidad', 'dependencia', 'organismo', 'municipio_ayuntamiento', 'unidad_responsable', 'unidad_presupuestal', 'inversion_federal', 'inversion_estatal', 'inversion_municipal', 'inversion_otros', 'inversion_total', 'ramo_presupuestal', 'descripcion', 'situacion_sin_proyecto', 'objetivos', 'metas', 'gasto_programable', 'tiempo_ejecucion', 'modalidad_ejecucion', 'programa_presupuestario', 'beneficiarios', 'normativa_aplicable', 'region', 'municipio', 'localidad', 'barrio_colonia', 'tipo_localidad', 'latitud', 'longitud', 'plan_nacional', 'plan_estatal', 'plan_municipal', 'acuerdos_transversales', 'ods', 'programas_SIE', 'indicadores_estrategicos', 'indicadores_estrategicos', 'observaciones', 'porcentaje_avance', 'estatus', 'situacion', 'retroalimentacion']

BLOCKED_FIELDS_PREFIX = "isBlocked_"
OBSERVATION_FIELDS_PREFIX = "observacion_"


@method_decorator(csrf_exempt, name='dispatch')
class ProjectView(View):
    """
    Vista basada en clases para la gestión de proyectos.
    
    Soporta los siguientes métodos:
      - GET:
          * Si se provee 'project_id', retorna el detalle de un proyecto.
          * Si no se provee, retorna una lista de proyectos con campos definidos.
      - POST:
          * Crea un nuevo proyecto utilizando FormProjectSerializer.
      - PUT:
          * Actualiza un proyecto existente (considerando campos bloqueados).
      - DELETE:
          * Elimina un proyecto según su 'project_id'.
    """

    def get(self, request, project_id=None):
        """
        Maneja la solicitud GET.
        
        Parámetros:
          - project_id (opcional): Si se provee, retorna los detalles de ese proyecto.
        
        Retorna:
          - JSON con los datos del proyecto o la lista de proyectos.
        """
        if project_id:
            project = get_object_or_404(FormProject, project_id=project_id)
            serializer = FormProjectSerializer(project)
            return JsonResponse(serializer.data, safe=False)
        else:
            projects = FormProject.objects.defer(
                *[f"{BLOCKED_FIELDS_PREFIX}{field}" for field in FIELDS_TO_FETCH],
                *[f"{OBSERVATION_FIELDS_PREFIX}{field}" for field in FIELDS_TO_FETCH]
            ).values(*FIELDS_TO_FETCH)
            return JsonResponse(list(projects), safe=False)

    def post(self, request):
        """
        Maneja la solicitud POST para crear un nuevo proyecto.
        
        Procedimiento:
          - Convierte el cuerpo de la solicitud a JSON.
          - Agrega el usuario actual (username) a los datos.
          - Valida y guarda el proyecto mediante FormProjectSerializer.
        """
        try:
            data = json.loads(request.body)
            data['user'] = request.user.username  # Agregar el usuario actual
            serializer = FormProjectSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'Project created successfully', 'project': serializer.data}, status=201)
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, project_id):
        """
        Maneja la solicitud PUT para actualizar un proyecto existente.
        
        Procedimiento:
          - Obtiene el proyecto a través de 'project_id'.
          - Itera sobre cada clave/valor del JSON recibido.
          - Actualiza los campos que no estén bloqueados (verificación mediante el prefijo 'isBlocked_').
          - Guarda el proyecto actualizado.
        """
        try:
            project = get_object_or_404(FormProject, project_id=project_id)
            data = json.loads(request.body)
            for key, value in data.items():
                is_blocked = getattr(project, f"{BLOCKED_FIELDS_PREFIX}{key}", False)
                if not is_blocked:
                    setattr(project, key, value)
            project.save()
            return JsonResponse({'message': 'Project updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, project_id):
        """
        Maneja la solicitud DELETE para eliminar un proyecto.
        
        Procedimiento:
          - Obtiene el proyecto a través de 'project_id'.
          - Elimina el proyecto y retorna un mensaje de éxito.
          - En caso de no encontrar el proyecto, retorna error 404.
        """
        try:
            project = get_object_or_404(FormProject, project_id=project_id)
            project.delete()
            return JsonResponse({'message': 'Project deleted successfully'}, status=204)
        except FormProject.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def generate_project_id(entity_type, entity_name, sector, current_year):
    """
    Función para generar el 'project_id' de un proyecto.
    
    Parámetros:
      - entity_type: Tipo de entidad (ej. Dependencia, Organismo, etc.).
      - entity_name: Nombre de la entidad, determinado según el tipo.
      - sector: Sector del proyecto.
      - current_year: Año actual.
    
    Procedimiento:
      - Obtiene la sigla de la entidad y el código del sector.
      - Calcula un número consecutivo basado en la cantidad de proyectos creados en el año.
      - Concatena los elementos para formar el 'project_id'.
    
    Retorna:
      - El 'project_id' generado.
    """
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
    """
    API endpoint para crear un nuevo proyecto.
    
    Procedimiento:
      - Obtiene el año actual.
      - Extrae 'tipo_entidad', y según éste obtiene el nombre de la entidad ('dependencia', 'organismo' o 'municipio_ayuntamiento').
      - Verifica que existan 'tipo_entidad', 'entity_name' y 'sector'; de lo contrario retorna un error.
      - Genera el 'project_id' mediante la función generate_project_id.
      - Agrega el usuario autenticado a los datos.
      - Valida y guarda el proyecto utilizando FormProjectSerializer.
    
    Retorna:
      - Los datos del proyecto creado o errores de validación.
    """
    current_year = datetime.now().year
    data = request.data.copy()
    entity_type = data.get('tipo_entidad')
    mapping = {
        'Dependencia': data.get('dependencia'),
        'Organismo': data.get('organismo'),
        'Ayuntamiento': data.get('municipio_ayuntamiento')
    }
    entity_name = mapping.get(entity_type, None)
    sector = data.get('sector')

    if not entity_type or not entity_name or not sector:
        return Response({'error': 'Faltan datos necesarios para generar el ID del proyecto.'}, status=status.HTTP_400_BAD_REQUEST)

    project_id = generate_project_id(entity_type, entity_name, sector, current_year)
    data['project_id'] = project_id

    data['user'] = request.user.username  # Añadir el ID del usuario autenticado
    serializer = FormProjectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReactAppView(TemplateView):
    """
    Vista que renderiza la aplicación React.
    
    - Renderiza el template 'index.html', que generalmente carga la aplicación frontend.
    """
    template_name = "index.html"

class UpdateProjectView(APIView):
    """
    APIView para actualizar un proyecto de forma parcial.
    
    Método PUT:
      - Busca el proyecto a través de 'project_id'.
      - Valida y actualiza el proyecto utilizando FormProjectSerializer de manera parcial.
      - Retorna los datos actualizados o errores de validación.
    """
    def put(self, request, project_id):
        try:
            project = FormProject.objects.get(project_id=project_id)
        except FormProject.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FormProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Django view para cerrar sesión
from django.contrib.auth import logout

@csrf_exempt
def logout_view(request):
    """
    Vista para cerrar la sesión del usuario.
    
    Método POST:
      - Cierra la sesión y retorna un mensaje de éxito.
    Otros métodos:
      - Retorna error indicando que el método no está permitido.
    """
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Sesión cerrada con éxito'}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

class DocumentUploadView(APIView):
    """
    API endpoint para subir documentos a un proyecto específico.
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, project_id, format=None):
        # Se busca el proyecto mediante project_id
        project = get_object_or_404(FormProject, project_id=project_id)
        
        # Permitir la modificación de request.data
        request.data._mutable = True
        request.data['project'] = project.id
        serializer = DocumentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def refresh_csrf_token(request):
    """
    Vista para refrescar y retornar el token CSRF.
    
    Retorna:
      - Un JSON con la clave 'csrfToken' obtenida desde la cookie CSRF.
    """
    return JsonResponse({"csrfToken": request.META.get("CSRF_COOKIE")})


# Historaial 


# class ProjectView(View):
#     def put(self, request, project_id):
#         """
#         Maneja la actualización de un proyecto y almacena un historial de cambios.
#         """
#         project = get_object_or_404(FormProject, project_id=project_id)
#         data = json.loads(request.body)
#         user = request.user  # Usuario autenticado

#         changes = {}  # Diccionario para almacenar los cambios

#         for key, value in data.items():
#             is_blocked = getattr(project, f"isBlocked_{key}", False)

#             if not is_blocked:
#                 old_value = getattr(project, key, None)
#                 if old_value != value:
#                     changes[key] = {"antes": old_value, "después": value}
#                     setattr(project, key, value)

#         if changes:
#             project.last_modified_by = user
#             project.last_modified_at = datetime.now()
#             project.save()

#             # Guardar en el historial
#             FormProjectHistory.objects.create(
#                 project=project,
#                 user=user,
#                 changes=changes
#             )

#         return JsonResponse({'message': 'Proyecto actualizado con historial registrado'})


# class ProjectHistoryView(View):
#     def get(self, request, project_id):
#         """
#         Devuelve el historial de cambios de un proyecto.
#         """
#         project = get_object_or_404(FormProject, project_id=project_id)
#         history = project.history.order_by('-timestamp').values('user__username', 'timestamp', 'changes')

#         return JsonResponse(list(history), safe=False)


# ---------------------------------------------
# Vista para listar y crear CedulaRegistro
# ---------------------------------------------

class CedulaRegistroListCreateView(generics.ListCreateAPIView):
    queryset = CedulaRegistro.objects.select_related('user').all()  # Utilizamos select_related para traer el user
    serializer_class = CedulaRegistroSerializer
    lookup_field = 'projInvestment_id'

    def get_queryset(self):
        """
        Sobrescribimos get_queryset para permitir el filtrado opcional por usuario.
        """
        queryset = super().get_queryset()

        # Si el usuario está autenticado y no es staff o admin, filtrar por el usuario
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        # Obtener los datos necesarios para generar el ID
        unidad_responsable = serializer.validated_data.get('unidad_responsable')
        fecha_registro = serializer.validated_data.get('fecha_registro') or datetime.now().date()

        # Generar el ID del proyecto
        proj_investment_id = generate_proj_investment_id(unidad_responsable, fecha_registro)

        # Guardar el registro con el ID generado, asignando el usuario autenticado
        cedula_registro = serializer.save(projInvestment_id=proj_investment_id, user=self.request.user)

        # Procesar la carga de múltiples archivos para los anexos
        self.save_anexos(self.request.FILES, cedula_registro)

    def save_anexos(self, files, cedula_registro):
        # Aquí procesamos los archivos adjuntos
        for file_key in files:
            for file in files.getlist(file_key):
                AnexoProyecto.objects.create(cedula=cedula_registro, archivo=file, tipo_anexo=file_key)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Llamar a perform_create para generar y guardar el ID
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Vista para obtener, actualizar y eliminar un registro específico
class CedulaRegistroDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CedulaRegistro.objects.all()
    serializer_class = CedulaRegistroSerializer

    def get_object(self):
        projInvestment_id = self.kwargs['projInvestment_id']
        return get_object_or_404(CedulaRegistro, projInvestment_id=projInvestment_id)

    def perform_update(self, serializer):
        # Actualizar la cédula existente
        cedula_registro = serializer.save()

        # Procesar la carga de nuevos archivos en caso de que se actualicen
        self.save_anexos(self.request.FILES, cedula_registro)

    def save_anexos(self, files, cedula_registro):
        """
        Función para manejar la actualización de anexos.
        """
        anexo_fields = [
            'estudios_factibilidad', 'analisis_alternativas', 'validacion_normativa',
            'liberacion_derecho_via', 'analisis_costo_beneficio', 'expediente_tecnico_docu',
            'proyecto_ejecutivo', 'manifestacion_impacto_ambiental', 'fotografia_render_proyecto',
            'otros_estudios'
        ]

        for field in anexo_fields:
            if field in files:
                for file in files.getlist(field):
                    # Crear nuevos anexos asociados a la cédula
                    AnexoProyecto.objects.create(
                        cedula=cedula_registro,
                        tipo_anexo=field,
                        archivo=file
                    )



@api_view(['GET'])
def proyectos_totales(request):
    total_proyectos = CedulaRegistro.objects.count()
    return Response({'total_proyectos': total_proyectos}, status=status.HTTP_200_OK)

@api_view(['GET'])
def proyectos_por_unidad_responsable(request):
    data = CedulaRegistro.objects.values('unidad_responsable').annotate(total=Count('unidad_responsable')).order_by('-total')
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def proyectos_por_usuario(request):
    data = CedulaRegistro.objects.values('user__username').annotate(total=Count('user')).order_by('-total')
    return Response(data, status=status.HTTP_200_OK)

from django.db.models import Q

@api_view(['GET'])
def propuesta_campana(request):
    # Usamos Q para hacer una consulta insensible a mayúsculas/minúsculas y tildes
    si_count = CedulaRegistro.objects.filter(Q(propuesta_campana__iexact='si') | Q(propuesta_campana__iexact='sí')).count()
    no_count = CedulaRegistro.objects.filter(propuesta_campana__iexact='no').count()
    return Response({'Si': si_count, 'No': no_count}, status=status.HTTP_200_OK)


@api_view(['GET'])
def cual_propuesta(request):
    data = CedulaRegistro.objects.values('cual_propuesta').annotate(total=Count('cual_propuesta')).order_by('-total')
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def cobertura_proyecto(request):
    data = CedulaRegistro.objects.values('cobertura').annotate(total=Count('cobertura')).order_by('-total')
    return Response(data, status=status.HTTP_200_OK)


class ProjectIdListView(APIView):

    def get(self, request, *args, **kwargs):
        # Obtiene todos los projInvestment_id de la base de datos
        project_ids = CedulaRegistro.objects.values_list('projInvestment_id', flat=True)

        # Retorna la lista en formato JSON
        return Response({'project_ids': list(project_ids)})



class AnexosProyectoListView(generics.ListAPIView):
    serializer_class = AnexoProyectoSerializer

    def get_queryset(self):
        projInvestment_id = self.kwargs.get('projInvestment_id')

        if projInvestment_id:
            # Verificamos si hay más de un anexo relacionado con la cédula y los obtenemos todos
            cedula = get_object_or_404(CedulaRegistro, projInvestment_id=projInvestment_id)
            return AnexoProyecto.objects.filter(cedula=cedula)
        else:
            # Si no se proporciona 'projInvestment_id', devolvemos todos los anexos
            return AnexoProyecto.objects.all()



@staff_member_required
def logout_all_users(request):
    # Eliminar todas las sesiones activas
    Session.objects.all().delete()
    
    # Opcionalmente, puedes mostrar un mensaje de éxito
    messages.success(request, "Se ha cerrado la sesión de todos los usuarios.")
    
    # Redirigir a alguna página (por ejemplo, al panel de administración o inicio)
    return redirect('admin:index')


# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable
# from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
# from reportlab.lib import colors
# from django.http import HttpResponse
# import io
# from django.shortcuts import get_object_or_404

# def generate_pdf(request, project_id):
#     buffer = io.BytesIO()
    
#     doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
#     styles = getSampleStyleSheet()

#     # Definir nuevos estilos
#     styles.add(ParagraphStyle(name='CustomTitle', parent=styles['Heading1'], fontSize=18, alignment=TA_CENTER, spaceAfter=10, textColor=colors.HexColor('#691B32')))
#     styles.add(ParagraphStyle(name='CustomSubTitle', parent=styles['Heading2'], fontSize=14, spaceAfter=10, textColor=colors.HexColor('#A02142')))
#     styles.add(ParagraphStyle(name='CustomBody', alignment=TA_JUSTIFY, fontSize=12, spaceAfter=10, leading=15, textColor=colors.HexColor('#707271')))
#     styles.add(ParagraphStyle(name='CustomCenter', alignment=TA_CENTER, fontSize=12, textColor=colors.HexColor('#707271')))
#     styles.add(ParagraphStyle(name='CustomFooter', alignment=TA_CENTER, fontSize=10, textColor=colors.HexColor('#98989A'), spaceBefore=20))
#     styles.add(ParagraphStyle(name='LabelStyle', fontSize=10, textColor=colors.HexColor('#A02142'), fontName='Helvetica-Bold'))

#     project = get_object_or_404(FormProject, project_id=project_id)

#     elements = []

#     # Encabezado con logo centrado fuera del margen
#     logo_url = "https://buenaspracticas.hidalgo.gob.mx/img/Logotipo.png"
#     logo_width, logo_height = 2.5 * inch, 0.35 * inch
#     logo = Image(logo_url, logo_width, logo_height)
#     logo.hAlign = 'CENTER'
#     elements.append(logo)
#     elements.append(Spacer(1, 20))

#     # Título del documento centrado
#     elements.append(Paragraph(f"Proyecto: {project.nombre_proyecto}", styles['CustomTitle']))
#     elements.append(Spacer(1, 20))

#     # Línea divisoria
#     elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#A02142'), spaceBefore=10, spaceAfter=20, hAlign='CENTER', vAlign='BOTTOM', dash=None))
#     elements.append(Spacer(1, 12))

#     # Subtítulo y detalles del proyecto
#     elements.append(Paragraph("Detalles del Proyecto", styles['CustomSubTitle']))
#     elements.append(Spacer(1, 12))

#     # Detalles en una sola columna
#     single_column_details = [
#         ("Descripción", project.descripcion),
#         ("Situación Sin Proyecto", project.situacion_sin_proyecto),
#         ("Objetivos", project.objetivos),
#     ]

#     for label, value in single_column_details:
#         elements.append(Paragraph(f"<font face='Helvetica-Bold' color='#A02142'>{label}:</font>", styles['LabelStyle']))
#         elements.append(Paragraph(value, styles['CustomBody']))
#         elements.append(Spacer(1, 12))

#     elements.append(Spacer(1, 24))

#     # Crear una tabla para los detalles del proyecto
#     details = [
#         ("ID del Proyecto", str(project.project_id)),
#         ("Sector", project.sector),
#         ("Dependencia", project.dependencia),
#         ("Organismo", project.organismo),
#         ("Municipio", project.municipio_ayuntamiento),
#         ("Monto Federal", f"${project.monto_federal:,.2f}"),
#         ("Monto Estatal", f"${project.monto_estatal:,.2f}"),
#         ("Monto Municipal", f"${project.monto_municipal:,.2f}"),
#         ("Monto Otros", f"${project.monto_otros:,.2f}"),
#         ("Inversión Estimada", f"${project.inversion_estimada:,.2f}"),
#         ("Región", project.region),
#         ("Localidad", project.localidad),
#         ("Municipio", project.municipio),
#         ("Barrio/Colonia/Ejido", project.barrio_colonia_ejido),
#         ("Latitud", str(project.latitud)),
#         ("Longitud", str(project.longitud)),
#         ("ODS", project.ods)
#     ]

#     # Organizar detalles en una tabla de dos columnas
#     detail_table_data = []
#     for i in range(0, len(details), 2):
#         row = []
#         for j in range(2):
#             if i + j < len(details):
#                 label, value = details[i + j]
#                 cell_content = Paragraph(f"<font face='Helvetica-Bold' color='#A02142'>{label}:</font> {value}", styles['CustomBody'])
#                 row.append(cell_content)
#             else:
#                 row.append('')
#         detail_table_data.append(row)

#     detail_table = Table(detail_table_data, colWidths=[3.25 * inch, 3.25 * inch])
#     detail_table.setStyle(TableStyle([
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#707271')),
#     ]))

#     elements.append(detail_table)
#     elements.append(Spacer(1, 24))

#     # Pie de página
#     elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#A02142'), spaceBefore=20, spaceAfter=10, hAlign='CENTER', vAlign='BOTTOM', dash=None))
#     elements.append(Spacer(1, 10))
#     elements.append(Paragraph("Gracias por su atención!", styles['CustomFooter']))
#     elements.append(Paragraph("contacto@buenaspracticas.hidalgo.gob.mx | buenaspracticas.hidalgo.gob.mx", styles['CustomFooter']))

#     doc.build(elements)

#     buffer.seek(0)
#     response = HttpResponse(buffer, content_type='application/pdf')
#     response['Content-Disposition'] = f'inline; filename="{project.project_id}.pdf"'
#     return response