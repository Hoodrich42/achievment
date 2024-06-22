from django.http import HttpResponseForbidden


class AuthenticatedMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(AuthenticatedMixin, self).dispatch(request, *args, **kwargs)