from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Core, Boost

class CoreSerializer(ModelSerializer):
    class Meta:
        model = Core
        fields = ['coins', 'click_power', 'auto_click_power', 'next_level_price']

    next_level_price = SerializerMethodField()

    def get_next_level_price(self, obj):
        return obj.calculate_next_level_price()
        
class BoostSerializer(ModelSerializer): 
    class Meta: 
        model = Boost 
        fields = '__all__'