from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from .views import activityView


urlpatterns = [
    path('activity/<slug:slug>/', activityView, name='activity'),
]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
else:
    # Configuration classique pour le développement local
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)