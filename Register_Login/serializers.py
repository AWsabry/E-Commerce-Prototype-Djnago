from rest_framework import serializers

from categories_and_products.models import Product

class Profileserializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'