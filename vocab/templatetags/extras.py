from django import template
from vocab.models import Question,Task_Result
register=template.Library()
@register.filter(name='get_item')
def get_item(id):
    obj=Task_Result.objects.filter(sno=id)[0]
    ques=Question.objects.filter(sno__gte=obj.s_range,sno__lte=obj.e_range)
    
    return ques
