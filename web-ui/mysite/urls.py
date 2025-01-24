from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path('grid/', include("grid.urls")),
    path("polls/", include("polls.urls")),
    path('admin/', admin.site.urls),
    path('eval/', include("eval.urls")),
    
]
