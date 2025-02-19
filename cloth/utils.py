from datetime import datetime, timedelta
from django.db.models import Q

from .models import Statistics

def parse_date(date_str):
    """Normalize and parse date from stored string format (d/m/YYYY) while handling extra spaces."""
    try:
        if not date_str or date_str.strip() == "":
            return None  # Return None if the string is empty
        normalized_date = date_str.strip().replace("\\", "/")
        return datetime.strptime(normalized_date, "%d/%m/%Y").date()
    except ValueError:
        return None  # Handle invalid date formats safely

def get_recent_cloth_operations(days=1):
    """
    Fetch and return cloth_operations from the Statistics model where the date is within the last 'days' days.

    Args:
        days (int): The number of days to go back (default is 1 day).

    Returns:
        dict: A dictionary with sorted lists of operations (newest first).
    """
    today = datetime.today().date()
    start_date = today - timedelta(days=days)

    all_cloth_operations = {"وارد": [], "قص": [], "مرتجع": []}

    # Define operation headers and keys
    operation_headers = {
        "وارد": ["كود الخامه", "اسم الخامه", "اللون", "عدد الاتواب", "الوزن", "التاريخ", "اسم المصبغة"],
        "قص": ["كود الخامه", "اسم الخامه", "اللون", "عدد الاتواب", "الوزن", "التاريخ", "رقم الموديل"],
        "مرتجع": ["كود الخامه", "اسم الخامه", "اللون", "عدد الاتواب", "الوزن", "التاريخ", "رقم الموديل"],
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

        all_cloth_operations[movement_type].extend(model_list)

    # Sort each list by date (newest first)
    for key in all_cloth_operations:
        all_cloth_operations[key] = sorted(all_cloth_operations[key], key=lambda obj: obj["date"], reverse=True)

    return all_cloth_operations
