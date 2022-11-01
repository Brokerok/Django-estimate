from rest_framework import viewsets, permissions
from .models import Pdf
from .serializers import PdfSerializer


class PdfViewSet(viewsets.ModelViewSet):
    queryset = Pdf.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = PdfSerializer
