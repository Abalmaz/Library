from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from api import views

schema_view = get_swagger_view(title='Library API')

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('book/', views.BookList.as_view()),
    # path('book/<pk>/', views.BookDetail.as_view()),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('swagger/', schema_view),
 ]