from django.urls import path
from .views import *

urlpatterns = [
    path('app/list', MessagesList.as_view(), name="Messages"),
    path('new/', crear_mensaje, name="New_message"),
    path('<pk>/', MessageDetail.as_view(), name="Message_detail"),
    path('delete/<pk>', MessageDelete.as_view(), name="Delete_message"),
]
