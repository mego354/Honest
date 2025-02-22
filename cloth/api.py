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
            instance = Fabric.objects.filter(fabric_code=row['fabric_code']).first()
            try:
                if instance:
                    # Update the existing instance with new data
                    for field, value in row.items():
                        setattr(instance, field, value)
                    instance.save()
                else:
                    # Create a new instance if it doesn't exist
                    row['id'] = None
                    instance = Fabric.objects.create(**row)


                results['fabric'].append({'updated': instance.fabric_code})
            except Exception as e:
                errors['fabric'].append({'failure': e})

        # Process CutTransfer data
        for row in data.get('cut_data', []):
            instance = CutTransfer.objects.filter(fabric_code=row['fabric_code'], model_number=row['model_number']).first()
            try:
                if instance:
                    # Update the existing instance with new data
                    for field, value in row.items():
                        setattr(instance, field, value)
                    instance.save()
                else:
                    # Create a new instance if it doesn't exist
                    row['id'] = None
                    instance = CutTransfer.objects.create(**row)

                results['cut_transfer'].append({'updated': f"{instance.fabric_code} - {instance.model_number}"})
            except Exception as e:
                errors['cut_transfer'].append({'failure': e})

        # Process ReturnTransfer data
        for row in data.get('return_data', []):
            instance = ReturnTransfer.objects.filter(fabric_code=row['fabric_code'], model_number=row['model_number']).first()
            try:
                if instance:
                    # Update the existing instance with new data
                    for field, value in row.items():
                        setattr(instance, field, value)
                    instance.save()
                else:
                    # Create a new instance if it doesn't exist
                    row['id'] = None
                    instance = ReturnTransfer.objects.create(**row)

                results['return_transfer'].append({'updated': f"{instance.fabric_code} - {instance.model_number}"})
            except Exception as e:
                errors['return_transfer'].append({'failure': e})

        # Process Statistics data
        for row in data.get('statistics_data', []):
            instance = Statistics.objects.filter(id=row['id']).first()
            try:
                if instance:
                    # Update the existing instance with new data
                    for field, value in row.items():
                        setattr(instance, field, value)
                    instance.save()
                else:
                    # Create a new instance if it doesn't exist
                    instance = Statistics.objects.create(**row)

                results['statistics'].append({'updated': f"{instance.id} - {instance.movement_type}"})
            except Exception as e:
                errors['statistics'].append({'failure': e})

        if any(errors[key] for key in errors):
            logging.error("Errors during processing: %s", errors)
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        Updates.objects.create()
        return Response({"results": results}, status=status.HTTP_201_CREATED)