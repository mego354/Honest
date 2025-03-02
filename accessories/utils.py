from datetime import datetime, timedelta
from django.db.models import Q

from .models import *


def get_recent_access_models(days=1):
    """
    Fetch and return access_models from the Statistics model where the date is within the last 'days' days.

    Args:
        days (int): The number of days to go back (default is 1 day).

    Returns:
        dict: A dictionary with sorted lists of operations (newest first).
    """
    today = datetime.today().date()
    start_date = today - timedelta(days=days)

    all_access_models = {"وارد": [], "قص": [], "مرتجع": []}

    # Define operation headers and keys
    models_headers = {
        "الكرتون": {
            "models": [CartonStock, CartonSupplies, PackagingCarton, ReturnCarton],
            "uniqunes_fields": ['model_number', 'length', 'width', 'height'],
            "sum_fields": ['total_quantity'],
        },
        "الشماعات": {
            "models": [HangerStock, HangerSupplies, PackagingHanger, ReturnHanger],
            "uniqunes_fields": ['hanger_number', 'color'],
            "sum_fields": ['sets_count', 'hangers_count'],
        },
        "السيزر": {
            "models": [SizerStock, SizerSupplies, PackagingSizer, ReturnSizer],
            "uniqunes_fields": ['size', 'color'],
            "sum_fields": ['sizer_count'],
        },
        "الاكياس": {
            "models": [BagStock, BagSupplies, PackagingBag, ReturnBag],
            "uniqunes_fields": ['bag_length', 'bag_width'],
            "sum_fields": ['bags_quantity'],
        },
        "هانج تاج": {
            "models": [HangTagStock, HangTagSupplies, PackagingHangTag, ReturnHangTag],
            "uniqunes_fields": ['type'],
            "sum_fields": ['quantity'],
        },
        "هيت سيل": {
            "models": [HeatSealStock, HeatSealSupplies, PackagingHeatSeal, ReturnHeatSeal],
            "uniqunes_fields": ['type'],
            "sum_fields": ['quantity'],
        },
        "تكت ستان": {
            "models": [TicketSatanStock, TicketSatanSupplies, PackagingTicketSatan, ReturnTicketSatan],
            "uniqunes_fields": ['model_number', 'size', 'cotton_percentage', 'polyester_percentage', 'upc_number'],
            "sum_fields": ['pieces_count'],
        },
        "تكت رئيسي": {
            "models": [TicketStock, TicketSupplies, PackagingTicket, ReturnTicket],
            "uniqunes_fields": ['type', 'size'],
            "sum_fields": ['pieces_count'],
        },
        "تكت برايس": {
            "models": [TicketPriceStock, TicketPriceSupplies, PackagingTicketPrice, ReturnTicketPrice],
            "uniqunes_fields": ['model_number'],
            "sum_fields": ['total'],
        },
        "كاردون": {
            "models": [KardonStock, KardonSupplies, PackagingKardon, ReturnKardon],
            "uniqunes_fields": ['color'],
            "sum_fields": ['meters_count'],
        },
        "استك": {
            "models": [RubberStock, RubberSupplies, PackagingRubber, ReturnRubber],
            "uniqunes_fields": ['width'],
            "sum_fields": ['total_weight'],
        },
        "خيط": {
            "models": [ThreadStock, ThreadSupplies, PackagingThread],
            "uniqunes_fields": ['thread_code'],
            "sum_fields": ['spools_count'],
        },
        "لزق": {
            "models": [GlueStock, GlueSupplies, PackagingGlue],
            "uniqunes_fields": ['width'],
            "sum_fields": ['cartons_count'],
        }
    }
    operation_key = {
        "كود الخامه": "fabric_code",
        "اسم الخامه": "fabric_name",
        "اللون": "color",
        "عدد الاتواب": "roll",
        "الوزن": "weight",
        "التاريخ": "date",
        "اسم المصبغة": "dyehouse_name",
        "رقم الموديل": "model_number",
    }

    # Filter instances by date range
    instances = Statistics.objects.filter(Q(date__isnull=False))
    filtered_instances = [
        obj for obj in instances if (parsed_date := parse_date(obj.date)) and start_date <= parsed_date <= today
    ]

    # Group instances by movement type
    models = {
        "وارد": [obj for obj in filtered_instances if obj.movement_type == "وارد"],
        "قص": [obj for obj in filtered_instances if obj.movement_type == "قص"],
        "مرتجع": [obj for obj in filtered_instances if obj.movement_type == "مرتجع"],
    }

    for movement_type, objects in models.items():
        if movement_type == "وارد":
            model_list = []
            unique_fabric_codes = set(obj.fabric_code for obj in objects)
            for fabric_code in unique_fabric_codes:
                fabric_code_models = [obj for obj in objects if obj.fabric_code == fabric_code]
                fabric_operation = {
                    "fabric_code": fabric_code,
                    "fabric_name": fabric_code_models[0].fabric_name or "------",
                    "detailed_level": len(fabric_code_models),
                    "roll": sum(obj.roll for obj in fabric_code_models),
                    "weight": sum(obj.weight for obj in fabric_code_models),
                    "date":  "------",
                    "operations": [
                        {key: getattr(obj, operation_key[key], "") for key in operation_headers[movement_type]}
                        for obj in fabric_code_models
                    ]
                }
                model_list.append(fabric_operation)
        else:
            model_list = []
            unique_model_fabric_pairs = set((obj.model_number, obj.fabric_code) for obj in objects)

            for model_number, fabric_code in unique_model_fabric_pairs:
                fabric_code_models = [obj for obj in objects if obj.model_number == model_number and obj.fabric_code == fabric_code]
                
                fabric_operation = {
                    "fabric_code": fabric_code or "------",
                    "fabric_name": fabric_code_models[0].fabric_name or "------",
                    "detailed_level": len(fabric_code_models),
                    "roll": sum(obj.roll for obj in fabric_code_models),
                    "weight": sum(obj.weight for obj in fabric_code_models),
                    "date": "------",
                    "operations": [
                        {key: getattr(obj, operation_key[key], "") for key in operation_headers[movement_type]}
                        for obj in fabric_code_models
                    ]
                }
                model_list.append(fabric_operation)

        all_access_models[movement_type].extend(model_list)

    # Sort each list by date (newest first)
    for key in all_access_models:
        all_access_models[key] = sorted(all_access_models[key], key=lambda obj: obj["date"], reverse=True)

    return all_access_models
