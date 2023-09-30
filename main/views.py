from django.shortcuts import render, redirect
from .models import Tasks
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views import View
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Index(View):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Invalid username or password")
            return redirect("/")

    def get(self, request):
        return render(request, 'index.html', {'title': "Vegetablemart"})


class Signup(View):
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirmPassword']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username already taken")
                return redirect("signup")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email already taken")
                return redirect("signup")
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    email=email)
                user.save()
                return redirect("/")
        else:
            messages.info(request, "password not matching")
            return redirect("signup")

    def get(self, request):
        return render(request, 'signup.html')


class Home(LoginRequiredMixin, View):
    def get(self, request):
        if request.user:
            all_tasks = Tasks.objects.all()
            return render(request, 'home.html', {'tasks':all_tasks})
        else:
             return redirect('index')
    
    def post(self,request):
        if 'CreateButton' in request.POST:
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            info = Tasks(tasktitle=title,taskdesc=desc)
            info.save()
            return redirect("home")


def updateTask(request, pk):
	task = Tasks.objects.get(id=pk)

	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('home')
	context = {'form':form}
	return render(request, 'Update.html', context)


class Delete(LoginRequiredMixin, View):
    def post(self,request,pk):
        if request.user.is_superuser or request.user.is_staff:
            task = Tasks.objects.get(id=pk)
            if 'DeleteButton' in request.POST:
                task.delete()
                return redirect("home")
        else:
            messages.info(request, "Your not authorized user to delete a task, please login with authorized details") 
            return redirect('index')
        
