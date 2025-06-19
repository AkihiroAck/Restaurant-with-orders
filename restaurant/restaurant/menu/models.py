from django.db import models


# Блюда
class Dish(models.Model):    
    name = models.CharField(max_length=255)  # Название
    description = models.TextField()  # Описание
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Цена
    category = models.CharField(max_length=50)  # Категорие
    
    def __str__(self):
        return self.name


# Заказы
class Order(models.Model):
    customer_name = models.CharField(max_length=255)  # Имя клиента
    dishes = models.ManyToManyField(Dish, related_name='orders')  # Блюда
    order_time = models.DateTimeField(auto_now_add=True)  # Время оформления заказа
    status = models.CharField(max_length=50, default='PENDING')  # Статус
    
    def __str__(self):
        return f'Order #{self.id}: {self.customer_name} - {self.status}'
    