from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum

from .models import *


def get_recent_access_models(days=1):
    """
    Fetch and return aggregated access models for each category within the last 'days' days.
    The operations are sorted by date (newest first).

    Args:
        days (int): The number of days to look back (default is 1 day).

    Returns:
        dict: A dictionary where each key is a category (e.g., "الكرتون") and the value is
              another dictionary with keys 'supply', 'package', and 'return' containing lists
              of operations.
    """
    today = now().date()
    start_date = today - timedelta(days=days)

    models_headers = {
        "الكرتون": {
            "models": [CartonSupplies, PackagingCarton, ReturnCarton],
            "uniqunes_fields": ['model_number', 'length', 'width', 'height'],
            "columns":[
                ["التاريخ","اسم المورد","رقم الموديل", "الطول", "العرض", "الارتفاع", "العدد الإجمالي"],
                ["التاريخ","المصنع","رقم الموديل", "العرض", "الارتفاع", "عدد الكرتون"],
                ["التاريخ","رقم الموديل", "العرض", "الارتفاع", "عدد الكرتون"],
                ], 
            "sum_fields": [['total_quantity'], ['carton_count'], ['carton_count']],
        },
        "الشماعات": {
            "models": [HangerSupplies, PackagingHanger, ReturnHanger],
            "uniqunes_fields": ['hanger_number', 'color'],
            "columns":[
                ["التاريخ","اسم المورد","رقم الشماعة","اللون","عدد الدست","عدد الشماعات"],
                ["التاريخ","المصنع","رقم الشماعة","اللون","عدد الدست","عدد الشماعات"],
                ["التاريخ","رقم الشماعة","اللون","عدد الدست","عدد الشماعات"],
                ], 
            "sum_fields": [['sets_count', 'hangers_count'], ['sets_count', 'hangers_count'], ['sets_count', 'hangers_count']],
        },
        "السيزر": {
            "models": [SizerSupplies, PackagingSizer, ReturnSizer],
            "uniqunes_fields": ['size', 'color'],
            "columns":[
                ["التاريخ","اسم المورد","المقاس","اللون","عدد السيزر"],
                ["التاريخ","المصنع","المقاس","اللون","عدد السيزر"],
                ["التاريخ","المقاس","اللون","عدد السيزر"],
                ], 
            "sum_fields": [['sizer_count'], ['sizer_count'], ['sizer_count']],
        },
        "الاكياس": {
            "models": [BagSupplies, PackagingBag, ReturnBag],
            "uniqunes_fields": ['bag_length', 'bag_width'],
            "columns":[
                ["التاريخ","اسم المورد","طول الكيس","العرض الكيس","الوزن","الاكياس في الكيلو","عدد الاكياس"],
                ["التاريخ","المصنع","طول الكيس","العرض الكيس","الوزن","عدد الاكياس"],
                ["التاريخ","طول الكيس","العرض الكيس","الوزن","عدد الاكياس"],
                ], 
            "sum_fields": [['bags_quantity'], ['bags_quantity'], ['bags_quantity']],
        },
        "هانج تاج": {
            "models": [HangTagSupplies, PackagingHangTag, ReturnHangTag],
            "uniqunes_fields": ['type'],
            "columns":[
                ["التاريخ","اسم المورد","النوع","العدد"],
                ["التاريخ","المصنع","النوع","العدد"],
                ["التاريخ","النوع","العدد"],
                ], 
            "sum_fields": [['quantity'], ['quantity'], ['quantity']],
        },
        "هيت سيل": {
            "models": [HeatSealSupplies, PackagingHeatSeal, ReturnHeatSeal],
            "uniqunes_fields": ['type'],
            "columns":[
                ["التاريخ","اسم المورد","النوع","المقاس","العدد"],
                ["التاريخ","المصنع","النوع","المقاس","العدد"],
                ["التاريخ","النوع","المقاس","العدد"],
                ], 
            "sum_fields": [['quantity'], ['quantity'], ['quantity']],
        },
        "تكت ستان": {
            "models": [TicketSatanSupplies, PackagingTicketSatan, ReturnTicketSatan],
            "uniqunes_fields": ['model_number', 'size', 'cotton_percentage', 'polyester_percentage', 'upc_number'],
            "columns":[
                ["التاريخ","اسم المورد","رقم الموديل","المقاس","القطن","البوليستر","UPC Number","عدد القطع"],
                ["التاريخ","المصنع","رقم الموديل","المقاس","القطن","البوليستر","UPC Number","عدد القطع"],
                ["التاريخ","رقم الموديل","المقاس","القطن","البوليستر","UPC Number","عدد القطع"],
                ], 
            "sum_fields": [['pieces_count'], ['pieces_count'], ['pieces_count']],
        },
        "تكت رئيسي": {
            "models": [TicketSupplies, PackagingTicket, ReturnTicket],
            "uniqunes_fields": ['type', 'size'],
            "columns":[
                ["التاريخ","اسم المورد","النوع","المقاس","عدد القطع"],
                ["التاريخ","المصنع","النوع","المقاس","عدد القطع"],
                ["التاريخ","النوع","المقاس","عدد القطع"],
                ], 
            "sum_fields": [['pieces_count'], ['pieces_count'], ['pieces_count']],
        },
        "تكت برايس": {
            "models": [TicketPriceSupplies, PackagingTicketPrice, ReturnTicketPrice],
            "uniqunes_fields": ['model_number'],
            "columns":[
                ["التاريخ","اسم المورد","الاجمالي","المقاس","رقم الموديل"],
                ["التاريخ","المصنع","الاجمالي","المقاس","رقم الموديل"],
                ["التاريخ","الاجمالي","المقاس","رقم الموديل"],
                ], 
            "sum_fields": [['total'], ['total'], ['total']],
        },
        "كاردون": {
            "models": [KardonSupplies, PackagingKardon, ReturnKardon],
            "uniqunes_fields": ['color'],
            "columns":[
                ["التاريخ","اسم المورد","عدد الامتار","اللون"],
                ["التاريخ","المصنع","عدد الامتار","اللون"],
                ["التاريخ","عدد الامتار","اللون"],
                ], 
            "sum_fields": [['meters_count'], ['meters_count'], ['meters_count']],
        },
        "استك": {
            "models": [RubberSupplies, PackagingRubber, ReturnRubber],
            "uniqunes_fields": ['width'],
            "columns":[
                ["التاريخ","اسم المورد","الوزن الاجمالي","عرض الاستك"],
                ["التاريخ","المصنع","الوزن الاجمالي","عرض الاستك"],
                ["التاريخ","الوزن الاجمالي","عرض الاستك"],
                ], 
            "sum_fields": [['total_weight'], ['total_weight'], ['total_weight']],
        },
        "خيط": {
            "models": [ThreadSupplies, PackagingThread],
            "uniqunes_fields": ['thread_code'],
            "columns":[
                ["التاريخ","اسم المورد","عدد البكر","اللون","كود الخيط"],
                ["التاريخ","المصنع","عدد البكر","اللون","كود الخيط"],
                ], 
            "sum_fields": [['spools_count'], ['spools_count'], ['spools_count']],
        },
        "لزق": {
            "models": [GlueSupplies, PackagingGlue],
            "uniqunes_fields": ['width'],
            "columns":[
                ["التاريخ","اسم المورد","عدد الكراتين","عرض اللزق"],
                ["التاريخ","المصنع","عدد الكراتين","عرض اللزق"],
                ], 
            "sum_fields": [['cartons_count'], ['cartons_count'], ['cartons_count']],
        }
    }

    all_access_models = []
    has_data = False
    for category, value in models_headers.items():
        access_model = {'model': category, 'models': value["models"], 'supply': {'operations': [], 'columns' : None}, 'package': {'operations': [], 'columns' : None}, 'return': {'operations': [], 'columns' : None}}

        # Iterate over the supply, packaging, and return models (skipping the first model, e.g. Stock)
        for index, model in enumerate(value["models"]):
            all_queryset = model.objects.filter(date__gte=start_date, date__lt=today)

            # Use .values() instead of .distinct()
            unique_queryset = all_queryset.values(*value["uniqunes_fields"]).annotate(total=Sum(value["sum_fields"][index][0]))
            if not has_data:
                has_data = len(unique_queryset) > 0


            for instance in unique_queryset: 
                filter_fields = {field: instance[field] for field in value["uniqunes_fields"]}
                items = all_queryset.filter(**filter_fields)

                if len(items) < 1 or not items:
                    continue
                elif len(items) == 1:
                    operations = [items[0]]
                else:
                    operations = [{field: instance["total"] for field in value["sum_fields"][index]}]
                    for item in items:
                        operations.append(item)

                if index == 0:
                    access_model['supply']['operations'] = operations
                    access_model['supply']['columns'] = value["columns"][index]
                elif index == 1:
                    access_model['package']['operations'] = operations
                    access_model['package']['columns'] = value["columns"][index]
                elif index == 2:
                    access_model['return']['operations'] = operations
                    access_model['return']['columns'] = value["columns"][index]

        all_access_models.append(access_model)

    return all_access_models if has_data else None
