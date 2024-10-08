from django.contrib import admin  
from django.urls import path, include   
from django.views.generic import RedirectView  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', include('quiz.urls')), 
    # path('', RedirectView.as_view(url='/register/', permanent=False)),  
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

