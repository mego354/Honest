from django.utils.timezone import now
from datetime import datetime, timedelta
from .models import ProductionPiece, Packing

from collections import defaultdict

def get_producion_models(days=1):
    """
    Retrieves unique models from productions created in the last `days` days.
    Includes total used_amount for each piece type.
    """
    productions = ProductionPiece.objects.filter(
        created_at__gt=now() - timedelta(days=days)
    )

    model_productions_map = defaultdict(list)
    type_totals_map = defaultdict(lambda: defaultdict(int))

    for production in productions:
        model = production.piece.model
        piece_type = production.piece.type

        model_productions_map[model].append({
            "type": piece_type,
            "size": production.piece.size,
            "created_at": production.created_at.strftime("%p %I:%M %Y/%m/%d"),
            "used_amount": production.used_amount,
            "factory": production.factory,
        })

        # Accumulate the total used_amount for each type in each model
        type_totals_map[model][piece_type] += production.used_amount

    recent_models = []
    
    for model, productions_details in model_productions_map.items():
        model_data = {
            "model": model,
            "productions": productions_details,
            "totals": [
                {"type": piece_type, "total_used_amount": total}
                for piece_type, total in type_totals_map[model].items()
            ]
        }
        recent_models.append(model_data)

    return recent_models

def get_packing_models(days=1):
    """
    Retrieves unique models from productions created in the last `days` days.
    Includes total used_amount for each piece type.
    """
    Packings = Packing.objects.filter(
        created_at__gt=now() - timedelta(days=days)
    )

    model_productions_map = defaultdict(list)
    type_totals_map = defaultdict(lambda: defaultdict(int))

    for Packing in Packings:
        model = Packing.piece.model

        model_productions_map[model].append({
            "carton": Packing.used_amount,
            "used_carton": Packing.used_carton,
            "created_at": Packing.created_at.strftime("%p %I:%M %Y/%m/%d"),
        })

        # Accumulate the total used_amount for each type in each model
        type_totals_map[model][piece_type] += Packing.used_amount

    recent_models = []
    
    for model, productions_details in model_productions_map.items():
        model_data = {
            "model": model,
            "productions": productions_details,
            "totals": [
                {"type": piece_type, "total_used_amount": total}
                for piece_type, total in type_totals_map[model].items()
            ]
        }
        recent_models.append(model_data)

    return recent_models
