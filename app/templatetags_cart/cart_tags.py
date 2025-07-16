from django import template

register = template.Library()

# subtotal
@register.filter
def mul(value, arg):
    try:
        return float(value) * int(arg)
    except (ValueError, TypeError):
        return 0
