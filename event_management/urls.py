from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home Page
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Apps
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('events/', include(('events.urls', 'events'), namespace='events')),
]

#  Media serve in dev mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
