from django.shortcuts import redirect, render
from django.http import HttpResponse 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .models import Core, Boost
from .serializers import CoreSerializer, BoostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

class Register(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST) 
        if form.is_valid(): 
            user = form.save() 
            login(request, user)
            core = Core(user=user)
            core.save()
            return redirect('index')
        return render(request, 'register.html', {'form': form})

class Login(APIView):
    form = UserForm()
    def get(self, request):
        return render(request, 'login.html', {'form': self.form})

    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password')) 
        if user:
            login(request, user) 
            return redirect('index')
        return render(request, 'login.html', {'form': self.form, 'invalid': True})

class User_logout(APIView):
    def get(self, request):
        logout(request)
        return redirect('login')

@login_required
def index(request): 
    core = Core.objects.get(user=request.user) 
    boosts = Boost.objects.filter(core=core) 
     
    return render(request, 'index.html', { 
        'core': core, 
        'boosts': boosts, 
    })

@api_view(['GET'])
@login_required
def call_click(request): 
    core = Core.objects.get(user=request.user) 
    is_levelup = core.click() 
    if is_levelup: 
        Boost.objects.create(core=core, price=core.coins, power=core.level*2) 
    core.save()

    return Response({ 'core': CoreSerializer(core).data, 'is_levelup': is_levelup })

class BoostViewSet(viewsets.ModelViewSet):  
    queryset = Boost.objects.all()  
    serializer_class = BoostSerializer

    def get_queryset(self): 
        core = Core.objects.get(user=self.request.user) 
        boosts = Boost.objects.filter(core=core) 
        return boosts
        
    def partial_update(self, request, pk):
        coins = request.data['coins']
        boost = self.queryset.get(pk=pk)

        is_levelup = boost.levelup(coins)
        if not is_levelup:
            return Response({ "error": "Не хватает денег" })

        old_boost_stats, new_boost_stats = is_levelup

        return Response({
            "old_boost_stats": self.serializer_class(old_boost_stats).data,
            "new_boost_stats": self.serializer_class(new_boost_stats).data,
    })

@api_view(['POST']) 
def update_coins(request): 
    coins = request.data['current_coins'] 
    core = Core.objects.get(user=request.user)
   
    is_levelup, boost_type = core.set_coins(coins) 
   
    if is_levelup: 
        Boost.objects.create(core=core, price=core.coins, power=core.level*2, type=boost_type) 
    core.save()

    return Response({
        'core': CoreSerializer(core).data, 
        'is_levelup': is_levelup,
    })

@api_view(['GET'])
def get_core(request):
    core = Core.objects.get(user=request.user)
    return Response({'core': CoreSerializer(core).data})
    
