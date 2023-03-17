from django.shortcuts import render,HttpResponse,redirect
from vocab.models import Question,Task_Result,userdetail

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import math
# Create your views here.






def home(request):
    if request.user.is_authenticated:
        task1=userdetail.objects.filter(user=request.user)
        # print(task1)
        progress=userdetail.objects.filter(user=request.user,test_status="True")
        # print(progress)
        c=0
        for i in progress:
            c+=i.points

        # print(c)
        Percent=math.ceil(c*100/300)
        # print(Percent)

        params={'task':task1,'user':request.user,'count':c,'percent':Percent}
        return render(request,"home1.html",params)
    else:
        task2=Task_Result.objects.filter(sno=1)
        print(task2)
        return render(request,'home2.html',{'task':task2})



def test(request,myid):
    global val,start,end
    if request.user.is_authenticated:
        if request.method=="POST":
            val=myid
            # print(myid)
            obj=Task_Result.objects.filter(sno=myid)[0]
            start=obj.s_range
            end=obj.e_range
    
            # print(obj)
            ques=Question.objects.filter(sno__gte=obj.s_range,sno__lte=obj.e_range)
            # print(ques)
            params={'ques':ques,'start':start}
            return render(request,"ques.html",params)
        else:
            return render(request,'404.html')
    else:
        if request.method=="POST":

            taskid=myid
            obj=Task_Result.objects.filter(sno=taskid)[0]
            start=obj.s_range
            end=obj.e_range
            # print(start,end)
            ques=Question.objects.filter(sno__gte=obj.s_range,sno__lte=obj.e_range)
            params={'ques':ques,'start':start}

            return render(request,"ques.html",params)
        else:
            return render(request,'404.html')






def result(request):
    try:
        global val,start,end
        # print(val)
        print(start,end)
        if request.method=="POST":
            if request.user.is_authenticated:

                res=request.POST.get('mytxt','')
                # print(res)
                res=res[:len(res)-1]
                choosen=res
                res1=res.split(',')
                obj=Question.objects.filter(sno__gte=start,sno__lte=end)
                # print(obj)
                # print(res1)
                p=0
                for i in range(len(obj)):
                    # print(obj[i].correct_opt)
                    if str(obj[i].correct_opt)==res1[i]:
                        p+=1
                # print("TOTAL POINTS",p)
                userdetail.objects.filter(user=request.user,task=Task_Result.objects.filter(sno=val)[0]).update(test_status="True",points=p,user_choosen=choosen)
                userdetail.objects.filter(user=request.user,task=Task_Result.objects.filter(sno=val+1)[0]).update(test_unlock="True")
        
                return redirect("/")
            
            else:
                res=request.POST.get('mytxt','')
                print(res)
                res=res[:len(res)-1]
                choosen=res
                res1=res.split(',')
                p=0
                obj=Question.objects.filter(sno__gte=start,sno__lte=end)

                for i in range(len(obj)):
                    # print(obj[i].correct_opt)
                    if str(obj[i].correct_opt)==res1[i]:
                        p+=1
                print("TOTAL POINTS",p)
                messages.success(request,f'You scored {p} points out of 10.To do more task and review your wrong answer SignUp! ')
                return redirect('/')


                

        else:
            return render(request,'404.html')
    
    except:
        return render(request,'404.html')






def handleSignup(request):
    if request.method=='POST':
        # get the post parameter
        username=request.POST.get('username','')
        name=request.POST.get('name','')
        signup_email=request.POST.get('signup_email','')
        password=request.POST.get('password','')
        password1=request.POST.get('password1','')
        # print(username,name,signup_email,password,password1)
        if len(name.split())!=2:
            messages.error(request,'Enter your full name')
            return redirect('signup')

        fname=name.split()[0]
        lname=name.split()[1]
        # username should be atleast 10 character long
        if len(username)>10:
            messages.error(request,'username must be under 10 characters')
            return redirect('signup')
        # username should be alphanumeric
        
        if not  username.isalnum():
            messages.error(request,'username should only cantain letters and number')
            return redirect('signup')
        # password should be match with confirm password field
        if password!=password1:
            messages.error(request,'Password does not match')
            return redirect('signup')

        
        myuser=User.objects.create_user(username,signup_email,password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        
        userdetail2=userdetail(user=username,task=Task_Result.objects.filter(sno=1)[0],test_unlock="True")

        userdetail2.save()

        for i in range(2,8):
            userdetail2=userdetail(user=username,task=Task_Result.objects.filter(sno=i)[0])
            userdetail2.save()

        
        user=authenticate(username=username, password=password)
        login(request,user)


        messages.success(request,"Your DoVocab's account successfully created")
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


def attempt_history(request):
    userdetail1=userdetail.objects.filter(user=request.user,test_status="True")
    # print(userdetail1)
    return render(request,'Attempt.html',{'user':userdetail1})



def refresh(request):
    # print(request.user)
    task=Task_Result.objects.all()
    for i in range(len(task)):
        userdetail2=userdetail.objects.filter(user=request.user,task=task[i])
        if len(userdetail2)>=1:
            # print('true')
            status=(userdetail2[0].test_unlock)
        else:
            if status=="True":
                
                userdetail2=userdetail(user=request.user,task=task[i],test_unlock="True")
                userdetail2.save()
                status=None

            
            else:
                userdetail2=userdetail(user=request.user,task=task[i])
                userdetail2.save()
        # print(userdetail2)
            

    return redirect('/')