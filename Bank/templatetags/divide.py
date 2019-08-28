from django import template
register = template.Library()

@register.filter
def ffdividef(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def iidividei(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def fidividef(value, arg):
    try:
        return float(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def ifdividef(value, arg):
    try:
        return int(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def fidividei(value, arg):
    try:
        return int(float(value) / int(arg))
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def ifdividei(value, arg):
    try:
        return int(int(value) / float(arg))
    except (ValueError, ZeroDivisionError):
        return None
