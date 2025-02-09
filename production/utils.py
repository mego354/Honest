from django.utils.timezone import now
from datetime import datetime, timedelta
from .models import ProductionPiece

def get_recent_models(days=1):
    """
    Retrieves unique models from productions created in the last 3 days.
    """
    productions = ProductionPiece.objects.filter(
        created_at__gt=now() - timedelta(days=days)
    )

    model_productions_map = {}

    for production in productions:
        model = production.piece.model
        if model not in model_productions_map:
            model_productions_map[model] = []

        model_productions_map[model].append({
            "type": production.piece.type,
            "size": production.piece.size,
            "created_at":  production.created_at.strftime("%p %I:%M %Y/%m/%d"),
            "used_amount": production.used_amount,
            "factory": production.factory,
        })

    recent_models = [
        {"model": model, "productions": productions_details}
        for model, productions_details in model_productions_map.items()
    ]

    return recent_models
