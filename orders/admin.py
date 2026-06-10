from django.contrib import admin
from .models import Order, OrderItem, Payment, Shipment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price_at_time", "get_total")

    def get_total(self, obj):
        return obj.quantity * obj.price_at_time

    get_total.short_description = "جمع کل"


class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    readonly_fields = ("amount", "status", "authority", "ref_id", "created_at")


class ShipmentInline(admin.StackedInline):
    model = Shipment
    extra = 0
    readonly_fields = (
        "shipping_cost",
        "tracking_code",
        "shipped_at",
        "delivered_at",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "final_amount",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user__phone", "id")

    inlines = [OrderItemInline, PaymentInline, ShipmentInline]

    fieldsets = (
        (
            "مشخصات سفارش",
            {
                "fields": (
                    "user",
                    "address",
                    "status",
                )
            },
        ),
        (
            "مبالغ",
            {
                "fields": (
                    "total_price",
                    "discount_amount",
                    "final_amount",
                )
            },
        ),
        (
            "تاریخ‌ها",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price_at_time", "total_price")

    def total_price(self, obj):
        return obj.quantity * obj.price_at_time

    total_price.short_description = "جمع کل"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "amount",
        "status",
        "authority",
        "ref_id",
        "created_at",
    )
    list_filter = ("status",)
    readonly_fields = ("created_at",)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "tracking_code",
        "shipping_cost",
        "shipped_at",
        "delivered_at",
    )
    readonly_fields = ("shipped_at", "delivered_at")
