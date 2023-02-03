from django.shortcuts import render,HttpResponse
from vocab.models import Question,Task_Result
# Create your views here.


def home(request):
    ques=Question.objects.filter(sno__gte=1,sno__lte=4)
    print(ques)
    params={'ques':ques}
    return render(request,"ques.html",params)




def home1(request):
    task=Task_Result.objects.filter()
    params={'task':task}
    return render(request,"home.html",params)



def test(request,myid):
    global val
    val=myid
    print(myid)
    obj=Task_Result.objects.filter(sno=myid)[0]
    
    print(obj)
    ques=Question.objects.filter(sno__gte=obj.s_range,sno__lte=obj.e_range)
    print(ques)
    params={'ques':ques}
    return render(request,"ques.html",params)



def result(request):
    global val
    print(val)
    if request.method=="POST":
        res=request.POST.get('mytxt','')
        res=res[:len(res)-1]
        res1=res.split(',')
        obj=Question.objects.all()
        p=0
        for i in range(len(obj)):
            print(obj[i].correct_opt)
            if obj[i].correct_opt==res1[i]:
                p+=1
        print("TOTAL POINTS",p)
        Task_Result.objects.filter(sno=val).update(points=p,test_status="True")
        Task_Result.objects.filter(sno=val+1).update(test_unlock="True")
        return HttpResponse("yes")

