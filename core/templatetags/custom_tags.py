from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def price_badge(value):
    try:
        return f'€{Decimal(value):.2f}'
    except (TypeError, ValueError, InvalidOperation):
        return value


@register.filter
def stars(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return ''

    value = max(0, min(value, 5))
    return '★' * value + '☆' * (5 - value)


@register.simple_tag
def booking_status_class(status):
    return {
        'Pending': 'badge-pending',
        'Approved': 'badge-approved',
        'Rejected': 'badge-rejected',
        'Cancelled': 'badge-cancelled',
        'Completed': 'badge-completed',
    }.get(status, 'bg-light text-dark border')

