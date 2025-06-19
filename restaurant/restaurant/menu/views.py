
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Dish, Order
from .serializers import DishSerializer, OrderSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    http_method_names = ['get', 'post', 'delete']

    
    # def destroy(self, request, *args, **kwargs):
    #     dish = self.get_object()

    #     # все заказы, в которых есть это блюдо
    #     orders_with_dish = Order.objects.filter(dishes=dish)

    #     for order in orders_with_dish:
    #         order.dishes.remove(dish)  # удалить блюдо из заказа

    #         # если больше нет блюд — удаляем заказ
    #         # if order.dishes.count() == 0:
    #         #     order.delete()  

    #     dish.delete()  # удаляем само блюдо

    #     return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


    def destroy(self, request, *args, **kwargs):
        order = self.get_object()

        if order.status != 'PENDING':
            return Response(
                {'error': 'Отменить можно только заказы в статусе "PENDING"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'CANCELLED'
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        
        # Валидация статуса
        if not new_status:
            return Response(
                {"error": "Статус не указан"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Правила смены статуса
        status_flow = {
            'PENDING': ['PREPARING'],
            'PREPARING': ['DELIVERING'],
            'DELIVERING': ['COMPLETED'],
        }
        
        current_status = order.status
        allowed_next = status_flow.get(current_status, [])
        
        if new_status not in allowed_next:
            return Response(
                {'error': f'Недопустимый переход статуса из "{current_status}" в "{new_status}"'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
    