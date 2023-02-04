from django.shortcuts import render,HttpResponse,redirect
from vocab.models import Question,Task_Result

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.






def home(request):
    task=Task_Result.objects.filter()
    params={'task':task,'user':request.user}
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





def handleSignup(request):
    if request.method=='POST':
        # get the post parameter
        username=request.POST.get('username','')
        name=request.POST.get('name','')
        signup_email=request.POST.get('signup_email','')
        password=request.POST.get('password','')
        password1=request.POST.get('password1','')
        print(username,name,signup_email,password,password1)
        fname=name.split()[0]
        lname=name.split()[1]
        # username should be atleast 10 character long
        if len(username)>10:
            messages.error(request,'username must be under 10 characters')
            return redirect('/')
        # username should be alphanumeric
        
        if not  username.isalnum():
            messages.error(request,'username should only cantain letters and number')
            return redirect('/')
        # password should be match with confirm password field
        if password!=password1:
            messages.error(request,'Password does not match')
            return redirect('/')

        
        myuser=User.objects.create_user(username,signup_email,password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your FlyHigh account successfully created")
        return redirect('/')


    else:
        return render(request,'signup.html')


def handleLogin(request):
    if request.method=='POST':
        loginusername=request.POST.get('username','')
        loginpassword=request.POST.get('password','')
        user=authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged in")
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials, Please Try Again')
            return redirect('/')



        
    else:
        return render(request,'login.html')


def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully Logout')
    return redirect('/')
