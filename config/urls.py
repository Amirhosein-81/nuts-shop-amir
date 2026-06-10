from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    CustomTokenObtainPairView,
    RegisterView,
    UserProfileView,
    UpdateUserProfileView,
    ChangePasswordView,
    LogoutView,
)



urlpatterns = [
    # Jet admin
    path('jet/', include('jet.urls', 'jet')),

    # Django admin
    path('admin/', admin.site.urls),

    # ---------------- AUTH ----------------
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),

    # ---------------- USER ----------------
    path('api/user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/user/profile/update/', UpdateUserProfileView.as_view(), name='update_profile'),
    path('api/user/change-password/', ChangePasswordView.as_view(), name='change_password'),

    # ---------------- ADDRESS (Router در users) ----------------
    path('api/user/', include('users.urls')),

    
    #------------------product ----------------------------------
    path("api/", include("products.urls")),

    #-------------------------cart--------------------------------
    
    path('api/cart/', include('cart.urls')),


    # favicon
    path(
        "favicon.ico",
        RedirectView.as_view(url="/static/favicon.ico", permanent=True),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
