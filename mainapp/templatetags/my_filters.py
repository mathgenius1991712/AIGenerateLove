from django import template
from ..models import Type
register = template.Library()
types = Type.objects.all()

@register.filter
def index(sequence, position):
    return sequence[position]


@register.filter
def display_who(type):
    print(type)
    type_id = type.get("id")
    if type_id == 1:
        return 'Mum'
    elif type_id == 2:
        return 'Dad'
    elif type_id == 3:
        return 'Wife'
    elif type_id == 4:
        return 'Husband'
    elif type_id == 5:
        return 'Grandma'
    elif type_id == 6:
        return 'Grandad'
    elif type_id == 7:
        return 'Girlfriend'
    elif type_id == 8:
        return 'Boyfriend'
    else:
        return 'Unknown type'

@register.filter
def display_gender(type):
    type_id = type.get("id")
    if type_id % 2 == 1:
        return 'she'
    elif type == 2:
        return 'he'
    else:
        return 'Unknown type'

