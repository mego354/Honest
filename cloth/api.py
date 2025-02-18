from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny

class PopulateModelsView(APIView):
    authentication_classes = []  # No authentication
    permission_classes = [AllowAny]  # Allow anyone to access (still protected by passcode)

    def post(self, request):
        # Validate passcode
        passcode = request.headers.get('X-API-PASSCODE')  # Passcode in headers
        if not passcode or passcode != settings.SECURE_API_PASSCODE:
            return Response({"error": "Forbidden: Invalid passcode."}, status=status.HTTP_403_FORBIDDEN)

        # Proceed with data processing
        data = request.data  # Expect a dictionary with keys for each model

        if not isinstance(data, dict):
            return Response({"error": "Invalid data format. Expected a dictionary."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = request.GET.get('refresh')
        if refresh:
            days = 2
            today = datetime.today().date()
            start_date = today - timedelta(days=days)

            Fabric.objects.filter(date__gte=start_date).delete()
            CutTransfer.objects.filter(date__gte=start_date).delete()
            ReturnTransfer.objects.filter(date__gte=start_date).delete()
            Statistics.objects.filter(date__gte=start_date).delete()
        else:
            Fabric.objects.all().delete()
            CutTransfer.objects.all().delete()
            ReturnTransfer.objects.all().delete()
            Statistics.objects.all().delete()

        errors = {}
        results = {}

        for row in data.get('fabric_data', []):  # Process only if the list is available
            serializer = FabricSerializer(data=row, many=False)  # Pass each row as a dictionary
            if serializer.is_valid():
                serializer.save()
                results['fabric'] = serializer.data
            else:
                errors['fabric'] = serializer.errors

        for row in data.get('cut_data', []):  # Process only if the list is available
            serializer = CutTransferSerializer(data=row, many=False)
            if serializer.is_valid():
                serializer.save()
                results['cut_transfer'] = serializer.data
            else:
                errors['cut_transfer'] = serializer.errors

        for row in data.get('return_data', []):  # Process only if the list is available
            serializer = ReturnTransferSerializer(data=row, many=False)
            if serializer.is_valid():
                serializer.save()
                results['return_transfer'] = serializer.data
            else:
                errors['return_transfer'] = serializer.errors

        for row in data.get('statistics_data', []):  # Process only if the list is available
            serializer = StatisticsSerializer(data=row, many=False)
            if serializer.is_valid():
                serializer.save()
                results['statistics'] = serializer.data
            else:
                errors['statistics'] = serializer.errors

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        Updates.objects.create()

        return Response({"results": results}, status=status.HTTP_201_CREATED)
