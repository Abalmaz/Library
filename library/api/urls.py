from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from api import views

schema_view = get_swagger_view(title='Library API')

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/facebook/connect/', views.FacebookConnect.as_view(),
         name='fb_connect'),
    path('rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('rest-auth/google/connect/', views.GoogleConnect.as_view(),
         name='google_connect'),
    path('swagger/', schema_view),
 ]