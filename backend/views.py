from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from rest_framework.views import APIView
from rest_framework.response import Response


class Register(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)  
        if form.is_valid():  
            user = form.save()  
            login(request, user)  
            return redirect('index') 
        return render(request, 'register.html', {'form': form})

class User_login(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = UserForm()
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('index')
        return render(request, 'login.html', {'form': form, 'invalid': True})

class User_logout(APIView):
    def get(self, request):
        logout(request)
        return redirect('login')