from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class PublisherRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is publisher."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_publisher:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin(object):
    """Verify that the current user is publisher and owner."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.publisher_profile.publishing_house.pk != \
                self.get_object().publishing.pk:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
