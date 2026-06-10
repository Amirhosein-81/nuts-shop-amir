from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer 
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def validate_product_id(self, value):
        from products.models import Product
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("این محصول وجود ندارد.")
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key', 'items', 'total_price']