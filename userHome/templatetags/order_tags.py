from django import template

register = template.Library()

@register.filter
def progress_percentage(status):
    if status == 'Pending':
        return 50
    elif status == 'Success':
        return 100
    return 0

@register.filter
def status_class(status):
    if status == 'Pending':
        return 'bg-warning'
    elif status == 'Success':
        return 'bg-success'
    return 'bg-secondary'
