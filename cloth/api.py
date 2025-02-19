from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny
from django.db import IntegrityError

import logging

logging.basicConfig(level=logging.DEBUG)


def parse_date(date_str):
    """Normalize and parse date from stored string format (d/m/YYYY) while handling extra spaces."""
    try:
        if not date_str or date_str.strip() == "":
            return None  # Return None if the string is empty
        normalized_date = date_str.strip().replace("\\", "/")
        return datetime.strptime(normalized_date, "%d/%m/%Y").date()
    except ValueError:
        return None  # Handle invalid date formats safely

# Helper function to update or create a model instance
def update_or_create_instance(model, unique_fields, row, serializer_class):
    try:
        instance = None

        # Ensure required unique fields are present in the input
        filter_criteria = {field: row.get(field) for field in unique_fields if row.get(field)}

        if filter_criteria:
            try:
                instance = model.objects.get(**filter_criteria)
            except model.DoesNotExist:
                instance = None
            except model.MultipleObjectsReturned:
                logging.warning(f"Multiple records found for {model.__name__} with criteria {filter_criteria}. Using the first one.")
                instance = model.objects.filter(**filter_criteria).first()

        # Serialize & validate data
        serializer = serializer_class(instance, data=row, partial=True) if instance else serializer_class(data=row)

        if serializer.is_valid():
            saved_instance = serializer.save()
            return {"id": saved_instance.id, "message": "Updated" if instance else "Created"}
        else:
            return {"errors": serializer.errors}

    except IntegrityError as e:
        logging.error(f"Integrity error in {model.__name__}: {e}")
        return {"error": str(e)}
    except Exception as e:
        logging.error(f"Unexpected error in {model.__name__}: {e}")
        return {"error": str(e)}

class PopulateModelsView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        passcode = request.headers.get('X-API-PASSCODE')
        if not passcode or passcode != settings.SECURE_API_PASSCODE:
            return Response({"error": "Forbidden: Invalid passcode."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        # logging.debug("Received data: %s", data)

        refresh = request.GET.get('refresh')
        if refresh:
            days = 10
            today = datetime.today().date()
            start_date = today - timedelta(days=days)

            def safe_delete(model):
                instances = model.objects.all()
                filtered_instances = [obj for obj in instances if (parsed_date := parse_date(obj.date)) and start_date <= parsed_date]
                model.objects.filter(id__in=[obj.id for obj in filtered_instances]).delete()

            safe_delete(Fabric)
            safe_delete(CutTransfer)
            safe_delete(ReturnTransfer)
            safe_delete(Statistics)
        else:
            Fabric.objects.all().delete()
            CutTransfer.objects.all().delete()
            ReturnTransfer.objects.all().delete()
            Statistics.objects.all().delete()

        errors = {
            'fabric': [],
            'cut_transfer': [],
            'return_transfer': [],
            'statistics': [],
        }
        results = {
            'fabric': [],
            'cut_transfer': [],
            'return_transfer': [],
            'statistics': [],
        }

        # Process Fabric data
        for row in data.get('fabric_data', []):
            result = update_or_create_instance(Fabric, ['fabric_code'], row, FabricSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['fabric'].append(result)
            else:
                results['fabric'].append(result)

        # Process CutTransfer data
        for row in data.get('cut_data', []):
            result = update_or_create_instance(CutTransfer, ['fabric_code', 'model_number'], row, CutTransferSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['cut_transfer'].append(result)
            else:
                results['cut_transfer'].append(result)

        # Process ReturnTransfer data
        for row in data.get('return_data', []):
            result = update_or_create_instance(ReturnTransfer, ['fabric_code', 'model_number'], row, ReturnTransferSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['return_transfer'].append(result)
            else:
                results['return_transfer'].append(result)

        # Process Statistics data
        for row in data.get('statistics_data', []):
            result = update_or_create_instance(Statistics, [], row, StatisticsSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['statistics'].append(result)
            else:
                results['statistics'].append(result)

        if any(errors[key] for key in errors):
            logging.error("Errors during processing: %s", errors)
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        Updates.objects.create()
        return Response({"results": results}, status=status.HTTP_201_CREATED)