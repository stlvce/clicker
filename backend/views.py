from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm


@login_required
def register(request): 
    if request.method == 'POST': 
        form = UserForm(request.POST) 
        if form.is_valid(): 
            user = form.save() 
            login(request, user) 
            return redirect('index')

        return render(request, 'register.html', {'form': form}) 
     
    form = UserForm() 
    return render(request, 'register.html', {'form': form})

def user_login(request):
    form = UserForm()
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('index')
        
        return render(request, 'login.html', {'form': form, 'invalid': True})

    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')