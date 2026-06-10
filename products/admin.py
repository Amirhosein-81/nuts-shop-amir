from django.contrib import admin
import jdatetime

from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
    ProductVariant,
)


# ===============================
# Inline for Product Images
# ===============================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt_text", "is_primary")
    show_change_link = True


# ===============================
# Inline for Product Variants
# ===============================
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ("title", "price", "stock", "sku")
    show_change_link = True


# ===============================
# Product Admin
# ===============================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "category", "jalali_created_at")
    list_filter = ("brand", "category")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductVariantInline, ProductImageInline]

    def jalali_created_at(self, obj):
        if not obj.created_at:
            return "-"
        j_date = jdatetime.datetime.fromgregorian(datetime=obj.created_at)
        return j_date.strftime("%Y/%m/%d - %H:%M")

    jalali_created_at.short_description = "تاریخ ایجاد"


# ===============================
# Category Admin
# ===============================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    prepopulated_fields = {"slug": ("name",)}


# ===============================
# Brand Admin
# ===============================
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)


# ثبت ساده بقیه مدل‌ها
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
