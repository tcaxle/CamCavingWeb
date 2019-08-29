from django import template
register = template.Library()


@register.filter()
def currency(value):
    # Formats any int or float as a string with 2dp and then appended £ sign
    value = str('{:.2f}'.format(value))
    if value.startswith('-'):
        return '- £ '+value.replace('-', '')
    else:
        return '+ £ '+value
