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

def get_recent_productions(models, days=5):
    """
    Fetch and return productions from the provided models where the date is within the last 'days' days.
    
    Args:
        models (list): A list of Django model classes.
        days (int): The number of days to go back (default is 4 days).
    
    Returns:
        list: A sorted list of model instances (newest first).
    """
    today = datetime.today().date()
    start_date = today - timedelta(days=days)

    all_productions = []
    for model in models:
        instances = model.objects.filter(Q(date__isnull=False))

        # Filter only productions within the date range
        filtered_instances = [
            obj for obj in instances if (parsed_date := parse_date(obj.date)) and start_date <= parsed_date <= today
        ]

        all_productions.extend(filtered_instances)

    # Sort by date (newest first)
    print(sorted(all_productions, key=lambda obj: parse_date(obj.date), reverse=True))
    return sorted(all_productions, key=lambda obj: parse_date(obj.date), reverse=True)
