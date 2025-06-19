from rest_framework import serializers
from .models import Order, Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    dishes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Dish.objects.all()
    )

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'order_time', 'status']

    def validate_dishes(self, value):
        if not value:
            raise serializers.ValidationError("Заказ должен содержать минимум одно блюдо")
        return value
    