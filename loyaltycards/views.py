from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Customer, Redemption
from .serializers import UserSerializer, CustomerSerializer, RedemptionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def retrieve(self, request, pk=None):
        if not request.user.is_staff and request.user.id != int(pk):
            return JsonResponse({'error': 'You are not authorized to view this customer.'}, status=403)
        queryset = Customer.objects.all()
        customer = get_object_or_404(queryset, pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class RedemptionViewSet(viewsets.ModelViewSet):
    queryset = Redemption.objects.all()
    serializer_class = RedemptionSerializer


@api_view(['POST'])
def login(request):
    user_id = request.data.get('user_id')
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')

    if user_id:
        user = get_object_or_404(User, id=user_id, is_active=True, is_staff=True)
    elif phone_number:
        customer = get_object_or_404(Customer, phone_number=phone_number, is_active=True)
        user = customer.user
    else:
        return Response({'error': 'Please provide user_id or phone_number.'}, status=400)

    if not user.check_password(password):
        return Response({'error': 'Invalid login credentials.'}, status=401)

    serializer = UserSerializer(user)
    return Response(serializer.data)
