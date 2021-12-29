import mainapp.views as mainapp
from django.urls.conf import include
from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", mainapp.main, name="main"),
    path("products/", include("mainapp.urls", namespace="products")),
    path("contact/", mainapp.contact, name="contact"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
