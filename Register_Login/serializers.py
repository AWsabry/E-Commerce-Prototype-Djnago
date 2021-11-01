from rest_framework import serializers
from .models import Product, Profile

class Profileserializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'