from django.urls import path, include

urlpatterns = [
    path('listings/', include('api.v1.listings.urls'))
]
