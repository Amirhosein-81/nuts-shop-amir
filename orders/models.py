from django.db import models
from django.conf import settings
from products.models import Product
from users.models import Address


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "سفارش ایجاد شد"
        PENDING = "pending", "در حال پرداخت"
        PAID = "paid", "پرداخت موفق"
        FAILED = "failed", "پرداخت ناموفق"
        CANCELED = "canceled", "لغو شده"
        SHIPPED = "shipped", "ارسال شده"
        DELIVERED = "delivered", "تحویل شده"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED
    )

    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.phone}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price_at_time

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        INIT = "init", "ایجاد شده"
        PENDING = "pending", "در انتظار پرداخت"
        SUCCESS = "success", "پرداخت موفق"
        FAILED = "failed", "پرداخت ناموفق"

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.INIT
    )

    # برای زرین‌پال: authority / ref_id
    authority = models.CharField(max_length=255, null=True, blank=True)
    ref_id = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order_id}"


class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipment")

    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tracking_code = models.CharField(max_length=255, null=True, blank=True)

    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Shipment for Order #{self.order_id}"
