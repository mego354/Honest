from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import (# 13 * 4 - 2 = 50
    CartonSupplies     , CartonStock     , PackagingCarton     , ReturnCarton,
    HangerSupplies     , HangerStock     , PackagingHanger     , ReturnHanger,
    SizerSupplies      , SizerStock      , PackagingSizer      , ReturnSizer,
    BagSupplies        , BagStock        , PackagingBag        , ReturnBag,
    HangTagSupplies    , HangTagStock    , PackagingHangTag    , ReturnHangTag,
    HeatSealSupplies   , HeatSealStock   , PackagingHeatSeal   , ReturnHeatSeal,
    TicketSatanSupplies, TicketSatanStock, PackagingTicketSatan, ReturnTicketSatan,
    TicketSupplies     , TicketStock     , PackagingTicket     , ReturnTicket,
    TicketPriceSupplies, TicketPriceStock, PackagingTicketPrice, ReturnTicketPrice,
    KardonSupplies     , KardonStock     , PackagingKardon     , ReturnKardon,
    RubberSupplies     , RubberStock     , PackagingRubber     , ReturnRubber,
    ThreadSupplies     , ThreadStock     , PackagingThread     , Updates,
    GlueSupplies       , GlueStock       , PackagingGlue       ,
)
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
            days = 2
            today = datetime.today().date()
            start_date = today - timedelta(days=days)

            def safe_delete(model):
                instances = model.objects.all()
                filtered_instances = [obj for obj in instances if (parsed_date := parse_date(obj.date)) and start_date <= parsed_date]
                model.objects.filter(id__in=[obj.id for obj in filtered_instances]).delete()

            safe_delete(CartonSupplies)
            safe_delete(CartonStock)
            safe_delete(PackagingCarton)
            safe_delete(ReturnCarton)
            safe_delete(HangerSupplies)
            safe_delete(HangerStock)
            safe_delete(PackagingHanger)
            safe_delete(ReturnHanger)
            safe_delete(SizerSupplies)
            safe_delete(SizerStock)
            safe_delete(PackagingSizer)
            safe_delete(ReturnSizer)
            safe_delete(BagSupplies)
            safe_delete(BagStock)
            safe_delete(PackagingBag)
            safe_delete(ReturnBag)
            safe_delete(HangTagSupplies)
            safe_delete(HangTagStock)
            safe_delete(PackagingHangTag)
            safe_delete(ReturnHangTag)
            safe_delete(HeatSealSupplies)
            safe_delete(HeatSealStock)
            safe_delete(PackagingHeatSeal)
            safe_delete(ReturnHeatSeal)
            safe_delete(TicketSatanSupplies)
            safe_delete(TicketSatanStock)
            safe_delete(PackagingTicketSatan)
            safe_delete(ReturnTicketSatan)
            safe_delete(TicketSupplies)
            safe_delete(TicketStock)
            safe_delete(PackagingTicket)
            safe_delete(ReturnTicket)
            safe_delete(TicketPriceSupplies)
            safe_delete(TicketPriceStock)
            safe_delete(PackagingTicketPrice)
            safe_delete(ReturnTicketPrice)
            safe_delete(KardonSupplies)
            safe_delete(KardonStock)
            safe_delete(PackagingKardon)
            safe_delete(ReturnKardon)
            safe_delete(RubberSupplies)
            safe_delete(RubberStock)
            safe_delete(PackagingRubber)
            safe_delete(ReturnRubber)
            safe_delete(ThreadSupplies)
            safe_delete(ThreadStock)
            safe_delete(PackagingThread)
            safe_delete(GlueSupplies)
            safe_delete(GlueStock)
            safe_delete(PackagingGlue)
        else:
            CartonSupplies.objects.all().delete()
            CartonStock.objects.all().delete()
            PackagingCarton.objects.all().delete()
            ReturnCarton.objects.all().delete()
            HangerSupplies.objects.all().delete()
            HangerStock.objects.all().delete()
            PackagingHanger.objects.all().delete()
            ReturnHanger.objects.all().delete()
            SizerSupplies.objects.all().delete()
            SizerStock.objects.all().delete()
            PackagingSizer.objects.all().delete()
            ReturnSizer.objects.all().delete()
            BagSupplies.objects.all().delete()
            BagStock.objects.all().delete()
            PackagingBag.objects.all().delete()
            ReturnBag.objects.all().delete()
            HangTagSupplies.objects.all().delete()
            HangTagStock.objects.all().delete()
            PackagingHangTag.objects.all().delete()
            ReturnHangTag.objects.all().delete()
            HeatSealSupplies.objects.all().delete()
            HeatSealStock.objects.all().delete()
            PackagingHeatSeal.objects.all().delete()
            ReturnHeatSeal.objects.all().delete()
            TicketSatanSupplies.objects.all().delete()
            TicketSatanStock.objects.all().delete()
            PackagingTicketSatan.objects.all().delete()
            ReturnTicketSatan.objects.all().delete()
            TicketSupplies.objects.all().delete()
            TicketStock.objects.all().delete()
            PackagingTicket.objects.all().delete()
            ReturnTicket.objects.all().delete()
            TicketPriceSupplies.objects.all().delete()
            TicketPriceStock.objects.all().delete()
            PackagingTicketPrice.objects.all().delete()
            ReturnTicketPrice.objects.all().delete()
            KardonSupplies.objects.all().delete()
            KardonStock.objects.all().delete()
            PackagingKardon.objects.all().delete()
            ReturnKardon.objects.all().delete()
            RubberSupplies.objects.all().delete()
            RubberStock.objects.all().delete()
            PackagingRubber.objects.all().delete()
            ReturnRubber.objects.all().delete()
            ThreadSupplies.objects.all().delete()
            ThreadStock.objects.all().delete()
            PackagingThread.objects.all().delete()
            GlueSupplies.objects.all().delete()
            GlueStock.objects.all().delete()
            PackagingGlue.objects.all().delete()

        errors = {
            'CartonSupplies': [],
            'CartonStock': [],
            'PackagingCarton': [],
            'ReturnCarton': [],
            'HangerSupplies': [],
            'HangerStock': [],
            'PackagingHanger': [],
            'ReturnHanger': [],
            'SizerSupplies': [],
            'SizerStock': [],
            'PackagingSizer': [],
            'ReturnSizer': [],
            'BagSupplies': [],
            'BagStock': [],
            'PackagingBag': [],
            'ReturnBag': [],
            'HangTagSupplies': [],
            'HangTagStock': [],
            'PackagingHangTag': [],
            'ReturnHangTag': [],
            'HeatSealSupplies': [],
            'HeatSealStock': [],
            'PackagingHeatSeal': [],
            'ReturnHeatSeal': [],
            'TicketSatanSupplies': [],
            'TicketSatanStock': [],
            'PackagingTicketSatan': [],
            'ReturnTicketSatan': [],
            'TicketSupplies': [],
            'TicketStock': [],
            'PackagingTicket': [],
            'ReturnTicket': [],
            'TicketPriceSupplies': [],
            'TicketPriceStock': [],
            'PackagingTicketPrice': [],
            'ReturnTicketPrice': [],
            'KardonSupplies': [],
            'KardonStock': [],
            'PackagingKardon': [],
            'ReturnKardon': [],
            'RubberSupplies': [],
            'RubberStock': [],
            'PackagingRubber': [],
            'ReturnRubber': [],
            'ThreadSupplies': [],
            'ThreadStock': [],
            'PackagingThread': [],
            'GlueSupplies': [],
            'GlueStock': [],
            'PackagingGlue': [],
        }
        results = {
            'CartonSupplies': [],
            'CartonStock': [],
            'PackagingCarton': [],
            'ReturnCarton': [],
            'HangerSupplies': [],
            'HangerStock': [],
            'PackagingHanger': [],
            'ReturnHanger': [],
            'SizerSupplies': [],
            'SizerStock': [],
            'PackagingSizer': [],
            'ReturnSizer': [],
            'BagSupplies': [],
            'BagStock': [],
            'PackagingBag': [],
            'ReturnBag': [],
            'HangTagSupplies': [],
            'HangTagStock': [],
            'PackagingHangTag': [],
            'ReturnHangTag': [],
            'HeatSealSupplies': [],
            'HeatSealStock': [],
            'PackagingHeatSeal': [],
            'ReturnHeatSeal': [],
            'TicketSatanSupplies': [],
            'TicketSatanStock': [],
            'PackagingTicketSatan': [],
            'ReturnTicketSatan': [],
            'TicketSupplies': [],
            'TicketStock': [],
            'PackagingTicket': [],
            'ReturnTicket': [],
            'TicketPriceSupplies': [],
            'TicketPriceStock': [],
            'PackagingTicketPrice': [],
            'ReturnTicketPrice': [],
            'KardonSupplies': [],
            'KardonStock': [],
            'PackagingKardon': [],
            'ReturnKardon': [],
            'RubberSupplies': [],
            'RubberStock': [],
            'PackagingRubber': [],
            'ReturnRubber': [],
            'ThreadSupplies': [],
            'ThreadStock': [],
            'PackagingThread': [],
            'GlueSupplies': [],
            'GlueStock': [],
            'PackagingGlue': [],
        }

        # Process Fabric data
        for row in data.get('CartonSupplies', []):
            result = update_or_create_instance(CartonSupplies, [], row, CartonSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['CartonSupplies'].append(result)
            else:
                results['CartonSupplies'].append(result)

        # Process CutTransfer data
        for row in data.get('CartonStock', []):
            result = update_or_create_instance(CartonStock, ['model_number', 'length', 'width', 'height'], row, CartonStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['CartonStock'].append(result)
            else:
                results['CartonStock'].append(result)

        # Process ReturnTransfer data
        for row in data.get('PackagingCarton', []):
            result = update_or_create_instance(PackagingCarton, [], row, PackagingCartonSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingCarton'].append(result)
            else:
                results['PackagingCarton'].append(result)

        # Process Statistics data
        for row in data.get('ReturnCarton', []):
            result = update_or_create_instance(ReturnCarton, [], row, ReturnCartonSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ReturnCarton'].append(result)
            else:
                results['ReturnCarton'].append(result)

        # Process Fabric data
        for row in data.get('HangerSupplies', []):
            result = update_or_create_instance(HangerSupplies, [], row, HangerSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['HangerSupplies'].append(result)
            else:
                results['HangerSupplies'].append(result)

        # Process CutTransfer data
        for row in data.get('HangerStock', []):
            result = update_or_create_instance(HangerStock, ['hanger_number', 'color'], row, HangerStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['HangerStock'].append(result)
            else:
                results['HangerStock'].append(result)

        # Process ReturnTransfer data
        for row in data.get('PackagingHanger', []):
            result = update_or_create_instance(PackagingHanger, [], row, PackagingHangerSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingHanger'].append(result)
            else:
                results['PackagingHanger'].append(result)

        # Process Statistics data
        for row in data.get('ReturnHanger', []):
            result = update_or_create_instance(ReturnHanger, [], row, ReturnHangerSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ReturnHanger'].append(result)
            else:
                results['ReturnHanger'].append(result)

        # Process Fabric data
        for row in data.get('SizerSupplies', []):
            result = update_or_create_instance(SizerSupplies, [], row, SizerSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['SizerSupplies'].append(result)
            else:
                results['SizerSupplies'].append(result)

        # Process CutTransfer data
        for row in data.get('SizerStock', []):
            result = update_or_create_instance(SizerStock, ['size', 'color'], row, SizerStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['SizerStock'].append(result)
            else:
                results['SizerStock'].append(result)

        # Process Fabric data
        for row in data.get('PackagingSizer', []):
            result = update_or_create_instance(PackagingSizer, [], row, PackagingSizerSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingSizer'].append(result)
            else:
                results['PackagingSizer'].append(result)

        # Process CutTransfer data
        for row in data.get('ReturnSizer', []):
            result = update_or_create_instance(ReturnSizer, [], row, ReturnSizerSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ReturnSizer'].append(result)
            else:
                results['ReturnSizer'].append(result)

        # Process ReturnTransfer data
        for row in data.get('BagSupplies', []):
            result = update_or_create_instance(BagSupplies, [], row, BagSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['BagSupplies'].append(result)
            else:
                results['BagSupplies'].append(result)

        # Process Statistics data
        for row in data.get('BagStock', []):
            result = update_or_create_instance(BagStock, ['bag_length', 'bag_width'], row, BagStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['BagStock'].append(result)
            else:
                results['BagStock'].append(result)

        # Process Fabric data
        for row in data.get('PackagingBag', []):
            result = update_or_create_instance(PackagingBag, [], row, PackagingBagSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingBag'].append(result)
            else:
                results['PackagingBag'].append(result)

        # Process CutTransfer data
        for row in data.get('ReturnBag', []):
            result = update_or_create_instance(ReturnBag, [], row, ReturnBagSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ReturnBag'].append(result)
            else:
                results['ReturnBag'].append(result)

        # Process ReturnTransfer data
        for row in data.get('HangTagSupplies', []):
            result = update_or_create_instance(HangTagSupplies, [], row, HangTagSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['HangTagSupplies'].append(result)
            else:
                results['HangTagSupplies'].append(result)

        # Process Statistics data
        for row in data.get('HangTagStock', []):
            result = update_or_create_instance(HangTagStock, ['type'], row, HangTagStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['HangTagStock'].append(result)
            else:
                results['HangTagStock'].append(result)

        # Process Fabric data
        for row in data.get('PackagingHangTag', []):
            result = update_or_create_instance(PackagingHangTag, [], row, PackagingHangTagSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingHangTag'].append(result)
            else:
                results['PackagingHangTag'].append(result)

        # Process CutTransfer data
        for row in data.get('ReturnHangTag', []):
            result = update_or_create_instance(ReturnHangTag, [], row, ReturnHangTagSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ReturnHangTag'].append(result)
            else:
                results['ReturnHangTag'].append(result)

        # Process Fabric data
        for row in data.get('HeatSealSupplies', []):
            result = update_or_create_instance(HeatSealSupplies, [], row, HeatSealSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['HeatSealSupplies'].append(result)
            else:
                results['HeatSealSupplies'].append(result)

        # Process CutTransfer data
        for row in data.get('HeatSealStock', []):
            result = update_or_create_instance(HeatSealStock, ['type'], row, HeatSealStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['HeatSealStock'].append(result)
            else:
                results['HeatSealStock'].append(result)

        # Process ReturnTransfer data
        for row in data.get('PackagingHeatSeal', []):
            result = update_or_create_instance(PackagingHeatSeal, [], row, PackagingHeatSealSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingHeatSeal'].append(result)
            else:
                results['PackagingHeatSeal'].append(result)

        # Process Statistics data
        for row in data.get('ReturnHeatSeal', []):
            result = update_or_create_instance(ReturnHeatSeal, [], row, ReturnHeatSealSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ReturnHeatSeal'].append(result)
            else:
                results['ReturnHeatSeal'].append(result)

        # Process Fabric data
        for row in data.get('TicketSatanSupplies', []):
            result = update_or_create_instance(TicketSatanSupplies, [], row, TicketSatanSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['TicketSatanSupplies'].append(result)
            else:
                results['TicketSatanSupplies'].append(result)

        # Process CutTransfer data
        for row in data.get('TicketSatanStock', []):
            result = update_or_create_instance(TicketSatanStock, ['model_number', 'size', 'cotton_percentage', 'polyester_percentage', 'upc_number'], row, TicketSatanStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['TicketSatanStock'].append(result)
            else:
                results['TicketSatanStock'].append(result)

        # Process ReturnTransfer data
        for row in data.get('PackagingTicketSatan', []):
            result = update_or_create_instance(PackagingTicketSatan, [], row, PackagingTicketSatanSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingTicketSatan'].append(result)
            else:
                results['PackagingTicketSatan'].append(result)

        # Process Statistics data
        for row in data.get('ReturnTicketSatan', []):
            result = update_or_create_instance(ReturnTicketSatan, [], row, ReturnTicketSatanSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ReturnTicketSatan'].append(result)
            else:
                results['ReturnTicketSatan'].append(result)

        # Process Fabric data
        for row in data.get('TicketSupplies', []):
            result = update_or_create_instance(TicketSupplies, [], row, TicketSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['TicketSupplies'].append(result)
            else:
                results['TicketSupplies'].append(result)

        # Process CutTransfer data
        for row in data.get('TicketStock', []):
            result = update_or_create_instance(TicketStock, ['type', 'size'], row, TicketStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['TicketStock'].append(result)
            else:
                results['TicketStock'].append(result)

        # Process Fabric data
        for row in data.get('PackagingTicket', []):
            result = update_or_create_instance(PackagingTicket, [], row, PackagingTicketSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingTicket'].append(result)
            else:
                results['PackagingTicket'].append(result)

        # Process CutTransfer data
        for row in data.get('ReturnTicket', []):
            result = update_or_create_instance(ReturnTicket, [], row, ReturnTicketSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ReturnTicket'].append(result)
            else:
                results['ReturnTicket'].append(result)

        # Process ReturnTransfer data
        for row in data.get('TicketPriceSupplies', []):
            result = update_or_create_instance(TicketPriceSupplies, [], row, TicketPriceSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['TicketPriceSupplies'].append(result)
            else:
                results['TicketPriceSupplies'].append(result)

        # Process Statistics data
        for row in data.get('TicketPriceStock', []):
            result = update_or_create_instance(TicketPriceStock, ['model_number'], row, TicketPriceStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['TicketPriceStock'].append(result)
            else:
                results['TicketPriceStock'].append(result)

        # Process Fabric data
        for row in data.get('PackagingTicketPrice', []):
            result = update_or_create_instance(PackagingTicketPrice, [], row, PackagingTicketPriceSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingTicketPrice'].append(result)
            else:
                results['PackagingTicketPrice'].append(result)

        # Process CutTransfer data
        for row in data.get('ReturnTicketPrice', []):
            result = update_or_create_instance(ReturnTicketPrice, [], row, ReturnTicketPriceSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ReturnTicketPrice'].append(result)
            else:
                results['ReturnTicketPrice'].append(result)

        # Process ReturnTransfer data
        for row in data.get('KardonSupplies', []):
            result = update_or_create_instance(KardonSupplies, [], row, KardonSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['KardonSupplies'].append(result)
            else:
                results['KardonSupplies'].append(result)

        # Process Statistics data
        for row in data.get('KardonStock', []):
            result = update_or_create_instance(KardonStock, ['color'], row, KardonStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['KardonStock'].append(result)
            else:
                results['KardonStock'].append(result)

        # Process Fabric data
        for row in data.get('PackagingKardon', []):
            result = update_or_create_instance(PackagingKardon, [], row, PackagingKardonSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingKardon'].append(result)
            else:
                results['PackagingKardon'].append(result)

        # Process CutTransfer data
        for row in data.get('ReturnKardon', []):
            result = update_or_create_instance(ReturnKardon, [], row, ReturnKardonSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ReturnKardon'].append(result)
            else:
                results['ReturnKardon'].append(result)

        # Process Fabric data
        for row in data.get('RubberSupplies', []):
            result = update_or_create_instance(RubberSupplies, [], row, RubberSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['RubberSupplies'].append(result)
            else:
                results['RubberSupplies'].append(result)

        # Process CutTransfer data
        for row in data.get('RubberStock', []):
            result = update_or_create_instance(RubberStock, ['width'], row, RubberStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['RubberStock'].append(result)
            else:
                results['RubberStock'].append(result)

        # Process ReturnTransfer data
        for row in data.get('PackagingRubber', []):
            result = update_or_create_instance(PackagingRubber, [], row, PackagingRubberSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingRubber'].append(result)
            else:
                results['PackagingRubber'].append(result)

        # Process Statistics data
        for row in data.get('ReturnRubber', []):
            result = update_or_create_instance(ReturnRubber, [], row, ReturnRubberSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ReturnRubber'].append(result)
            else:
                results['ReturnRubber'].append(result)

        # Process Fabric data
        for row in data.get('ThreadSupplies', []):
            result = update_or_create_instance(ThreadSupplies, [], row, ThreadSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ThreadSupplies'].append(result)
            else:
                results['ThreadSupplies'].append(result)

        # Process CutTransfer data
        for row in data.get('ThreadStock', []):
            result = update_or_create_instance(ThreadStock, ['thread_code'], row, ThreadStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['ThreadStock'].append(result)
            else:
                results['ThreadStock'].append(result)

        # Process ReturnTransfer data
        for row in data.get('PackagingThread', []):
            result = update_or_create_instance(PackagingThread, [], row, PackagingThreadSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingThread'].append(result)
            else:
                results['PackagingThread'].append(result)

        # Process Statistics data
        for row in data.get('GlueSupplies', []):
            result = update_or_create_instance(GlueSupplies, [], row, GlueSuppliesSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['GlueSupplies'].append(result)
            else:
                results['GlueSupplies'].append(result)

        # Process Fabric data
        for row in data.get('GlueStock', []):
            result = update_or_create_instance(GlueStock, ['width'], row, GlueStockSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['GlueStock'].append(result)
            else:
                results['GlueStock'].append(result)

        # Process CutTransfer data
        for row in data.get('PackagingGlue', []):
            result = update_or_create_instance(PackagingGlue, [], row, PackagingGlueSerializer)
            if isinstance(result, dict) and 'errors' in result:
                errors['PackagingGlue'].append(result)
            else:
                results['PackagingGlue'].append(result)


        if any(errors[key] for key in errors):
            logging.error("Errors during processing: %s", errors)
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        Updates.objects.create()
        return Response({"results": results}, status=status.HTTP_201_CREATED)