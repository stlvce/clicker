from django.urls import path
from . import views

boosts = views.BoostViewSet.as_view({   
    'get': 'list',  
    'post': 'create', 
})

urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.Register.as_view(), name='register'),
    path('login/',views.Login.as_view(), name='login'),
    path('logout/',views.User_logout.as_view(), name='logout'),
    path('call_click/', views.call_click),
    path('boosts/', boosts, name='boosts'),

    # changed
    path('buy_boost/', views.buy_boost), 
]