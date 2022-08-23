from django.contrib import admin
from django.urls import path, include
from blogApp.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', inicio),
    path('admin/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('App/', include('blogApp.urls')),
    path('chatApp/', include('chatApp.urls'))

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)