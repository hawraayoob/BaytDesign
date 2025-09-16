from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divide the value by the argument."""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def sub(value, arg):
    """Subtract the argument from the value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add(value, arg):
    """Add the argument to the value."""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def bhd(value):
    """Format the value as BHD currency."""
    try:
        # Convert to Decimal for precise decimal arithmetic
        value = Decimal(str(value))
        # Format with 3 decimal places and BHD symbol
        return f"BHD {value:.3f}"
    except (ValueError, TypeError, decimal.InvalidOperation):
        return "BHD 0.000"





