from django.urls import include, path
from django.contrib import admin


admin.autodiscover()

urlpatterns = [path('admin/', admin.site.urls)]

try:
    import grappelli.urls
except ImportError:
    pass
else:
    urlpatterns += [path("grappelli/", include(grappelli.urls))]
