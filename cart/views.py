from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_name
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

class CartView(APIView):
    permission_classes = [AllowAny] # همه کاربران (مهمان و عضو) باید به سبد خرید دسترسی داشته باشند

    def get_cart(self, request):
        """
        یک متد کمکی برای پیدا کردن یا ساختن سبد خرید بر اساس کاربر یا سشن
        """
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            return cart
        else:
            # اگر سشن وجود نداشت، یک سشن جدید ایجاد می‌کنیم
            if not request.session.session_key:
                request.session.create()
            cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
            return cart

    def get(self, request):
        """مشاهده سبد خرید و آیتم‌های داخل آن"""
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """افزودن محصول به سبد خرید یا افزایش تعداد آن"""
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({"error": "ارسال product_id الزامی است."}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        
        # بررسی اینکه آیا این محصول از قبل در سبد خرید هست یا نه
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            # اگر از قبل بود، تعدادش را اضافه می‌کنیم
            cart_item.quantity += quantity
        else:
            # اگر جدید بود، تعداد اولیه را ست می‌کنیم
            cart_item.quantity = quantity
        
        cart_item.save()
        return Response({"message": "محصول با موفقیت به سبد خرید اضافه شد."}, status=status.HTTP_201_CREATED)

    def patch(self, request):
        """ویرایش مستقیم تعداد یک محصول در سبد خرید"""
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id or quantity is None:
            return Response({"error": "ارسال product_id و quantity الزامی است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            quantity = int(quantity)
            if quantity <= 0:
                cart_item.delete()
                return Response({"message": "محصول به دلیل تعداد صفر از سبد حذف شد."}, status=status.HTTP_200_OK)
            
            cart_item.quantity = quantity
            cart_item.save()
            return Response({"message": "تعداد محصول به‌روزرسانی شد."}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "این محصول در سبد خرید شما یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        """حذف کامل یک محصول از سبد خرید"""
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "ارسال product_id الزامی است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({"message": "محصول از سبد خرید حذف شد."}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "این product_id در سبد خرید شما وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)