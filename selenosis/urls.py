import django
from django.conf.urls import include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = [url(r'^admin/', admin.site.urls)]

try:
    import grappelli.urls
except ImportError:
    pass
else:
    urlpatterns += [url(r"^grappelli/", include(grappelli.urls))]
