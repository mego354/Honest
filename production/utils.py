from django.utils.timezone import now
from datetime import timedelta
from .models import ProductionPiece

def get_recent_models():
    """
    Retrieves unique models from productions created in the last 3 days.
    """
    productions = ProductionPiece.objects.filter(
        created_at__gt=now() - timedelta(days=3)
    )

    model_productions_map = {}

    for production in productions:
        model = production.piece.model
        if model not in model_productions_map:
            model_productions_map[model] = []

        model_productions_map[model].append({
            "piece": production.piece,
            "created_at": production.created_at,
            "used_amount": production.used_amount,
            "factory": production.factory,
        })

    recent_models = [
        {"model": model, "productions": productions_details}
        for model, productions_details in model_productions_map.items()
    ]

    return recent_models
