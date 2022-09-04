
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('search.urls')),
    path('mysongusers/', include('django.contrib.auth.urls')),
    path('mysongusers/', include('mysongusers.urls')),
]
