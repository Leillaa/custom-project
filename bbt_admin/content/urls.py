from django.urls import path

from .views import MainContentViewSet

urlpatterns = [
    path('content/<int:telegram_id>', MainContentViewSet.as_view({
        'get': 'list'
    })),
    path('content/<int:telegram_id>/<int:pk>', MainContentViewSet.as_view({
        'get': 'retrieve',
        'post': 'create'
    })),
    path('content/back/<int:telegram_id>', MainContentViewSet.as_view({
        'get': 'back'
    })),
    path('content/media/<int:pk>',
         MainContentViewSet.as_view({
             'get': 'media',
             'post': 'media'
         })),
]
