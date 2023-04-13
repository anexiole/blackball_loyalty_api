from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Customer, Redemption
from .serializers import CustomerSerializer, RedemptionSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def redeem(request):
    phone_number = request.data.get('phone_number')
    points = request.data.get('points')

    customer = get_object_or_404(Customer, phone_number=phone_number)

    if customer.points < points:
        return Response({'error': 'Not enough points to redeem'}, status=status.HTTP_400_BAD_REQUEST)

    customer.points -= points
    customer.save()

    redemption = Redemption.objects.create(customer=customer, points_spent=points)

    waffle = False
    free_drink = False

    if redemption.id % 5 == 0:
        waffle = True
    if redemption.id % 10 == 0:
        free_drink = True

    return Response({'success': 'Redemption successful', 'waffle': waffle, 'free_drink': free_drink}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def point_balance(request, phone_number):
    customer = get_object_or_404(Customer, phone_number=phone_number)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def redemption_history(request, phone_number):
    customer = get_object_or_404(Customer, phone_number=phone_number)
    redemptions = Redemption.objects.filter(customer=customer)
    serializer = RedemptionSerializer(redemptions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def authorize_redemption(request, redemption_id):
    redemption = get_object_or_404(Redemption, id=redemption_id)

    if redemption.is_authorized:
        return Response({'error': 'Redemption has already been authorized'}, status=status.HTTP_400_BAD_REQUEST)

    redemption.is_authorized = True
    redemption.save()

    return Response({'success': 'Redemption authorized'}, status=status.HTTP_200_OK)
