from datetime import datetime, timedelta
from django.db.models import Q

from .models import Statistics

def parse_date(date_str):
    """Normalize and parse date from stored string format (d/m/YYYY) while handling extra spaces."""
    try:
        if not date_str or date_str.strip() == "":
            return None  # Return None if the string is empty
        normalized_date = date_str.strip().replace("\\", "/")  # Remove spaces & fix slashes
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

    # Filter instances by date range
    instances = Statistics.objects.filter(Q(date__isnull=False))
    filtered_instances = [
        obj for obj in instances if (parsed_date := parse_date(obj.date)) and start_date <= parsed_date <= today
    ]

    # Group instances by movement type
    models = {
        "Fabric": [obj for obj in filtered_instances if obj.movement_type == "وارد"],
        "CutTransfer": [obj for obj in filtered_instances if obj.movement_type == "قص"],
        "ReturnTransfer": [obj for obj in filtered_instances if obj.movement_type == "مرتجع"],
    }

    for model_type, objects in models.items():
        model_list = []
        unique_fabric_codes = set(obj.fabric_code for obj in objects)
        
        for fabric_code in unique_fabric_codes:
            fabric_code_models = [obj for obj in objects if obj.fabric_code == fabric_code]
            model_list.append(
                {
                    "fabric_code": fabric_code,
                    "roll": sum(obj.roll for obj in fabric_code_models),
                    "weight": sum(obj.weight for obj in fabric_code_models),
                    "date": max(parse_date(obj.date) for obj in fabric_code_models if obj.date),  # Ensuring sorting by latest date
                }
            )

        if model_type == "Fabric":
            all_cloth_operations["وارد"].extend(model_list)
        elif model_type == "CutTransfer":
            all_cloth_operations["قص"].extend(model_list)
        elif model_type == "ReturnTransfer":
            all_cloth_operations["مرتجع"].extend(model_list)

    # Sort each list by date (newest first)
    for key in all_cloth_operations:
        all_cloth_operations[key] = sorted(all_cloth_operations[key], key=lambda obj: obj["date"], reverse=True)

    return all_cloth_operations
