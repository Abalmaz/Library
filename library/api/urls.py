from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Library API')


urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/', schema_view),
 ]