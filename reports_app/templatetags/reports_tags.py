from django import template
register = template.Library()


@register.filter
def get_var_type(value):
    return type(value)