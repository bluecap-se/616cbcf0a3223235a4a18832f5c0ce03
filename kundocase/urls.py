from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('kundocase.forum.urls')),
    url(r'^api/', include('kundocase.rest_api.urls')),
]

# Set up static file serving for development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
