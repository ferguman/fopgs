from django.contrib import path
urlpatterns = [
    path('', csrf_exempt(pgqlv)),
]
