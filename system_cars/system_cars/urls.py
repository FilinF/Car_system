from django.urls import path
from rest_framework.routers import DefaultRouter
from applications.views import CarEntryViewSet, OperationsViewSet
from django.contrib import admin

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

router = DefaultRouter()
router.register(r'car', CarEntryViewSet, basename='car')



urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),

    path('admin/', admin.site.urls),
    path('operations/create/', OperationsViewSet.as_view({'post': 'export_data'}), name='export-data'),
    path('operations/new_oper/<uuid:operation_id>/', OperationsViewSet.as_view({'get': 'retrieve'}), name='get-operation'),

    path('car/', CarEntryViewSet.as_view({'post': 'create'}), name='create-route'),
    path('car/get_cars/', CarEntryViewSet.as_view({'get': 'get_cars'}), name='list-of-cars'),
    path('car/change_st/notifyed/<int:id>/', CarEntryViewSet.as_view({'get': 'notify'}), name='change-st-notifyed'),
] + router.urls