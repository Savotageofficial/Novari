from django.http import HttpResponse
from django.db.models import Q, Max
from datetime import datetime
import secrets

from novari_base.models import Product, AdminToken, User, Order

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# --- Helper Functions ---

def createproduct(name, description, price, color="white"):
    new_product = Product(name=name, description=description, price=price, color=color)
    new_product.save()
    return {
        'product_id': new_product.id,
        'name': new_product.name,
        'description': description,
        'price': price,
        'color': color
    }


def check_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    try:
        token = AdminToken.objects.get(token=auth_header)
        user = User.objects.get(id=token.user_id)
        return user
    except (AdminToken.DoesNotExist, User.DoesNotExist):
        return None


# --- Public Endpoints ---

class ProductListView(APIView):
    def get(self, request):
        color = request.GET.get('color', '')
        min_price = request.GET.get('min_price', 0)

        max_available_price = Product.objects.aggregate(Max('price'))['price__max'] or 0
        max_price = request.GET.get('max_price', max_available_price)

        results = Product.objects.filter(
            Q(color__contains=color) &
            Q(price__gte=min_price) &
            Q(price__lte=max_price)
        ).values('id', 'name', 'price', 'description', 'discount', 'color', 'image')

        return Response(list(results))


class ProductDetailView(APIView):
    def get(self, request, id):
        try:
            product = Product.objects.filter(id=id).values(
                'id', 'name', 'price', 'description', 'discount', 'color', 'image'
            ).first()
            if product is None:
                return Response({'error': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)
            return Response(product)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_admin:
            return Response({'error': 'Invalid credentials or insufficient privileges'}, status=status.HTTP_401_UNAUTHORIZED)

        token_value = secrets.token_urlsafe(32)
        admin_token = AdminToken.objects.create(user=user, token=token_value)

        return Response({
            'token': admin_token.token,
            'admin': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
            }
        })


# --- Admin Endpoints ---

class AdminProductsView(APIView):
    def get(self, request):
        user = check_token(request)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        results = Product.objects.all().values('id', 'name', 'price', 'description', 'discount', 'color', 'image')
        return Response(list(results))

    def post(self, request):
        user = check_token(request)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            name = request.data.get('name')
            price = request.data.get('price')
            description = request.data.get('description')
            color = request.data.get('color', 'white')
            product_data = createproduct(name, description, price, color)
            return Response(product_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Invalid, {e}'}, status=status.HTTP_400_BAD_REQUEST)


class AdminProductDeleteView(APIView):
    def patch(self, request, id):
        user = check_token(request)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({'error': f'Product {id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Only update fields that were actually sent
        if 'name' in request.data:
            product.name = request.data.get('name')
        if 'description' in request.data:
            product.description = request.data.get('description')
        if 'price' in request.data:
            product.price = request.data.get('price')
        if 'color' in request.data:
            product.color = request.data.get('color')
        if 'discount' in request.data:
            product.discount = request.data.get('discount')

        product.save()

        return Response({
            'success': f'Product {id} updated',
            'product': {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'color': product.color,
                'discount': product.discount,
            }
        })


    def delete(self, request, id):
        user = check_token(request)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            product = Product.objects.get(id=id)
            product.delete()
            return Response({'success': f'Product {id} deleted'})
        except Product.DoesNotExist:
            return Response({'error': f'Product {id} does not exist'}, status=status.HTTP_404_NOT_FOUND)


class SubmitOrderView(APIView):
    def post(self, request):
        try:
            new_order = Order(
                Email=request.data.get('email'),
                Phone=request.data.get('phone'),
                FirstName=request.data.get('firstname'),
                LastName=request.data.get('lastname'),
                Address=request.data.get('address'),
                city=request.data.get('city'),
                country=request.data.get('country'),
                payment_method=request.data.get('payment_method'),
                created_at=datetime.now(),
                Order_Notes=request.data.get('Order_Notes', ''),
            )
            new_order.save()
            return Response({'success': f'Order submitted at id {new_order.id}'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)