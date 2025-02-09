from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('book/', include("books.urls")),
    path('review/', include("reviews.urls")),
    path('user/', include("user.urls")),
    path('admin/', admin.site.urls),
]
