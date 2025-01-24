from django import template

register = template.Library()

@register.filter
def divide(value, divisor):
    try:
        return round(value / divisor)  # Round to 2 decimal places
    except (TypeError, ZeroDivisionError):
        return "N/A"
