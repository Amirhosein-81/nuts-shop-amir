from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address, OTP


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("phone", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("phone", "first_name", "last_name")
    ordering = ("phone",)

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("اطلاعات شخصی", {"fields": ("first_name", "last_name", "email")}),
        ("دسترسی‌ها", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("تاریخ‌ها", {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "password1", "password2", "is_staff", "is_active")}
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Address)
admin.site.register(OTP)
