from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, SocialConnectView

from rest_framework import viewsets, mixins, generics
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers import BookSerializer, AuthorDetailSerializer
from mylib.models import Book, Author


class AuthorDetail(mixins.RetrieveModelMixin,
                 generics.GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('title', 'authors', 'year', 'publishing')
    ordering_fields = ('title', 'year', 'authors')


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter