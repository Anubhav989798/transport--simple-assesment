from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.http import HttpResponseRedirect
from django.contrib.auth import login,logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import Question,Answer,like
from django.db.models import Count


@csrf_exempt
def SignUpView(request):
    if request.method=='GET':
        return render(request,'app/signUp.html')
    else:
        try:
            email=request.POST.get('email','').strip()
            username=request.POST.get('username','').strip()
            name=request.POST.get('name','').strip()
            password=request.POST.get('password','').strip()

            #regular expression for password
            if len(password)<8:
                raise ValueError("please provide password in atleast 8 character")
            #regular expression for email
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex,email):
                raise ValueError("please provide valid format of email")
            #validating username
            if len(username)==0:
                raise ValueError("please provide username")
            #validating firstname
            if len(name)==0:
                raise ValueError("name cannot be empty")
            #validating email
            if User.objects.filter(email=email).exists():
                raise ValueError("email already exist")
            #validating username
            if User.objects.filter(username=username).exists():
                raise ValueError("username already exist")
            
            
            user=User.objects.create_user(username=username,email=email,first_name=name)
            user.set_password(password)
            user.save()

            messages.success(request,"SignUp successfully")
            return HttpResponseRedirect('/login')
        except Exception as e:
                messages.error(request, str(e))
                return render(request, 'app/signUp.html')

@csrf_exempt
def LoginView(request):
    if request.method=='GET':
        return render(request,'app/login.html')
    else:
        try:
            username=request.POST.get('username','').strip()
            password=request.POST.get('password','').strip()

            if not User.objects.filter(username=username).exists():
                raise ValueError("username doesnot exists")
            user=User.objects.get(username=username)
            if not user.check_password(password):
                 raise ValueError("password is incorrect")
            login(request,user)
            messages.success(request,"login successfully")
            return redirect('/')
            
        except Exception as e:
                messages.error(request, str(e))
                return render(request, 'app/login.html')

def logoutView(request):
    logout(request)
    question_list=Question.objects.all().order_by('-created_at')
    context={
        'question':question_list,
    }
    return render(request,'app/home.html',context)
            

class homeView(View):
    def get(self,request,*args, **kwargs):
        question_list=Question.objects.all().order_by('-created_at')
        context={
           'question':question_list,
        }
        return render(request,'app/home.html',context)
    
#posting a question
class PostingQuestion(View):
    def get(self,request,*args, **kwargs):
        return render(request,'app/questionpost.html')
    
    @csrf_exempt
    def post(self,request,*args, **kwargs):
        question=request.POST.get('question','').strip()
        Question.objects.create(question=question,user_id=request.user.id)
        question_list=Question.objects.all().order_by('-created_at')
        context={
           'question':question_list,
        }
        return render(request,'app/home.html',context)

#Viewing posted answer 
class AnswerView(View):
    def get(self,request,pk):
        question_list=Question.objects.get(id=pk)
        answer=Answer.objects.filter(question_id=pk).annotate(c=Count('like')).order_by('-created_at')
        context={
           'question':question_list,
           'answer':answer
        }
        return render(request,'app/answerview.html',context)
    
#posting  answer 
class postAnswerView(View):
    def get(self,request,pk):
        return render(request,'app/answerpost.html',{'id':pk})
    
    @csrf_exempt
    def post(self,request,pk):
        try:
            answer=request.POST.get('answer','').strip()
            Answer.objects.create(answer=answer,question_id=pk,user_id=request.user.id)
            question_list=Question.objects.get(id=pk)
            answer=Answer.objects.filter(question_id=pk).annotate(c=Count('like')).order_by('-created_at')
            context={
            'question':question_list,
            'answer':answer
            }
            print("hello")
            return render(request,'app/answerview.html',context)
        except Exception as e:
            print(str(e))
            question_list=Question.objects.all().order_by('-created_at')
            context={
            'question':question_list,
            }
            return render(request,'app/home.html',context) 
        
#adding like to the answer
class likeView(View):
    @csrf_exempt
    def post(self,request,pk):
        try:
            if not like.objects.filter(answer_id=pk,user_id=request.user.id).exists():
                like.objects.create(answer_id=pk,user_id=request.user.id)
            ans=Answer.objects.get(id=pk)
            answer=Answer.objects.filter(question_id=ans.question_id).annotate(c=Count('like')).order_by('-created_at')
            question_list=Question.objects.get(id=ans.question_id)
            context={
            'question':question_list,
            'answer':answer
            }
            return render(request,'app/answerview.html',context) 
        except Exception as e:
            print(str(e))
            question_list=Question.objects.all().order_by('-created_at')
            context={
            'question':question_list,
            }
            return render(request,'app/home.html',context) 


