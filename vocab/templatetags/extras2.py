from django import template
from vocab.models import Question,Task_Result
register=template.Library()
@register.filter(name='check')
def check(val1,val2):
    value=val1.split(',')
    # print(type(value[val2-1]))
    return int(value[val2-1])
