from datetime import datetime, timedelta
from django.db.models import Q

def parse_date(date_str):
    """Normalize and parse date from stored string format (d/m/YYYY) while handling extra spaces."""
    try:
        if not date_str or date_str.strip() == "":
            return None  # Return None if the string is empty
        normalized_date = date_str.strip().replace("\\", "/")  # Remove spaces & fix slashes
        return datetime.strptime(normalized_date, "%d/%m/%Y").date()
    except ValueError:
        return None  # Handle invalid date formats safely

def get_recent_cloth_operations(models, days=1):
    """
    Fetch and return cloth_operations from the provided models where the date is within the last 'days' days.
    
    Args:
        models (list): A list of Django model classes.
        days (int): The number of days to go back (default is 4 days).
    
    Returns:
        list: A sorted list of model instances (newest first).
    """
    today = datetime.today().date()
    start_date = today - timedelta(days=days)

    all_cloth_operations = {"وارد": [], "قص": [], "مرتجع": [], "احصائيات": []}

    for model in models:
        instances = model.objects.filter(Q(date__isnull=False))

        # Filter only cloth_operations within the date range
        filtered_instances = [
            obj for obj in instances if (parsed_date := parse_date(obj.date)) and start_date <= parsed_date <= today
        ]

        # Determine the type of operation based on the model or some attribute
        # This is just an example, you need to adjust it based on your actual logic
        if model.__name__ == "Fabric":
            all_cloth_operations["وارد"].extend(filtered_instances)
        elif model.__name__ == "CutTransfer":
            all_cloth_operations["قص"].extend(filtered_instances)
        elif model.__name__ == "ReturnTransfer":
            all_cloth_operations["مرتجع"].extend(filtered_instances)
        elif model.__name__ == "Statistics":
            all_cloth_operations["احصائيات"].extend(filtered_instances)

    # Sort each list by date (newest first)
    for key in all_cloth_operations:
        all_cloth_operations[key] = sorted(all_cloth_operations[key], key=lambda obj: parse_date(obj.date), reverse=True)
    return all_cloth_operations

###############################################################################################################################

