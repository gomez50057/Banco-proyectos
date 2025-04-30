from rest_framework import viewsets
from .models import NivelacionTierra, ArchivoPDF
from .serializers import NivelacionTierraSerializer, ArchivoPDFSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class NivelacionTierraViewSet(viewsets.ModelViewSet):
    queryset = NivelacionTierra.objects.all()
    serializer_class = NivelacionTierraSerializer
    authentication_classes = []    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny] 

    
    def perform_create(self, serializer):
        # 1) Se crea la instancia sin los archivos (solo datos “no-file”).
        #    Esto dispara el save(), genera el folio y lo guarda en BD.
        instance = serializer.save(created_by=self.request.user)

        # 2) Ahora se reasigna los archivos desde request.FILES y se salva de nuevo.
        #    upload_to() ya verá instance.folio correctamente.
        archivo = self.request.FILES.get('archivo_pdf')
        constancia = self.request.FILES.get('constancia_pdf')

        if archivo:
            instance.archivo_pdf.save(archivo.name, archivo, save=False)
        if constancia:
            instance.constancia_pdf.save(constancia.name, constancia, save=False)

        # Se guarda la instancia con los nuevos archivos ya en la ruta correcta.
        instance.save()

class ArchivoPDFViewSet(viewsets.ModelViewSet):
    queryset = ArchivoPDF.objects.all()
    serializer_class = ArchivoPDFSerializer

    authentication_classes = []    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny] 

class NivelacionTierraViewSet(viewsets.ModelViewSet):
    """
    Con lookup_field='folio' el router creará:
      - GET   /formularios/           → lista
      - GET   /formularios/{folio}/   → detalle por folio
      - PUT, PATCH, DELETE sobre /formularios/{folio}/
    """
    queryset = NivelacionTierra.objects.all()
    serializer_class = NivelacionTierraSerializer
    authentication_classes = []    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny] 


    # Aquí indicamos que la parte dinámica de la URL es el campo `folio`
    lookup_field = 'folio'
    lookup_value_regex = '[^/]+'  # evita “/” en el folio

    def perform_create(self, serializer):
        # Guarda el usuario autenticado en created_by
        serializer.save(created_by=self.request.user)

class NivelacionTierraUserViewSet(viewsets.ModelViewSet):
    """
    Lista, crea, detalla, actualiza y borra solo las nivelaciones
    cuyo campo `created_by` es el usuario autenticado.
    
    Rutas generadas:
      - GET    /nivelaciones/          → lista de sus propios registros
      - POST   /nivelaciones/          → crear uno nuevo (se asigna created_by automáticamente)
      - GET    /nivelaciones/{pk}/     → detalle de uno propio
      - PUT    /nivelaciones/{pk}/     → actualizar (solo si es suyo)
      - PATCH  /nivelaciones/{pk}/
      - DELETE /nivelaciones/{pk}/     → eliminar (solo si es suyo)
    """
    serializer_class = NivelacionTierraSerializer
    authentication_classes = []
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny] 


    def get_queryset(self):
        # Filtra la lista para que solo aparezcan sus propias instancias
        return NivelacionTierra.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Al crear, asignamos siempre el usuario autenticado
        serializer.save(created_by=self.request.user)
