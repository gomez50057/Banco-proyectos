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

from django.contrib.auth.models import User, Group

from .models import FormProject
from .serializers import FormProjectSerializer, BulkCreateProjectSerializer, FormProjectSerializer 
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


@method_decorator(csrf_exempt, name='dispatch')
class BulkCreateUsers(View):
    def post(self, request):
        try:
            # Lee el cuerpo de la solicitud y conviértelo a un objeto JSON
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
    proyectos = FormProject.objects.filter(estatus__in=['Atendido', 'En Proceso']).values(
        'project_id', 'project_name', 'estatus', 'porcentaje_avance', 'observaciones'
    )
    return JsonResponse(list(proyectos), safe=False)

@login_required
def ver_proyectos_usuario(request):
    user = request.user
    proyectos = FormProject.objects.filter(user=user).values(
        'isBlocked_project','estatus' , 'project_id', 'project_name', 'estatus', 'porcentaje_avance', 'observaciones'
    )
    return JsonResponse(list(proyectos), safe=False)

class BulkCreateProjects(APIView):
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
                'isBlocked_project',
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
            data['user'] = request.user.username  # Agregar el usuario actual al proyecto
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

    data['user'] = request.user.username  # Añadir el ID del usuario autenticado
    serializer = FormProjectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReactAppView(TemplateView):
    template_name = "index.html"

class UpdateProjectView(APIView):
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
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Sesión cerrada con éxito'}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



from rest_framework import generics
from .models import CedulaRegistro
from .serializers import CedulaRegistroSerializer

from rest_framework import generics
from .models import CedulaRegistro
from .serializers import CedulaRegistroSerializer
from .utils import generate_proj_investment_id  # Importa la función utilitaria
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime

class CedulaRegistroListCreateView(generics.ListCreateAPIView):
    queryset = CedulaRegistro.objects.all()
    serializer_class = CedulaRegistroSerializer

    def perform_create(self, serializer):
        # Obtener los datos necesarios para generar el ID
        unidad_responsable = serializer.validated_data.get('unidad_responsable')
        fecha_registro = serializer.validated_data.get('fecha_registro', datetime.now().date())

        # Generar el ID
        proj_investment_id = generate_proj_investment_id(unidad_responsable, fecha_registro)

        # Guardar el registro con el ID generado
        serializer.save(projInvestment_id=proj_investment_id)

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




from django.contrib.sessions.models import Session
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

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
#     elements.append(Paragraph(f"Proyecto: {project.project_name}", styles['CustomTitle']))
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
#         ("Municipio", project.municipioEnd),
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