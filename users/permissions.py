from decouple import config
from rest_framework.permissions import AllowAny, BasePermission


class NotLoggedInPermission(AllowAny):
    """used when user not logged in (like verify email address)"""
    message = 'Permission Denied'

    def has_permission(self, request, view):
        """By default, headers key are been changed from
        LEADBOARD_SK_HEADER to Leadboard-Sk-Header that's why we change the key """
        for key, value in request.headers.items():
            #  check the host if we are running manage.py test and if it's on test
            #  mode we allow without the headers .
            #  Note if we pass in headers it provides errors with throttle_scope
            if request.get_host() == "testserver":
                return True
            if key.lower() == 'leadboard-sk-header':
                leadboard_sk_header = request.headers['Leadboard-Sk-Header']
                is_header = leadboard_sk_header == config('LEADBOARD_SK_HEADER')
                # fixme: throttle provide error when  credentials  is passed on TestCase
                return is_header


class LoggedInPermission(BasePermission):
    """
    Used when the user is logged in we only added this if other verification
    could be needed but right now we are only using the secret header
    """
    message = "Permission Denied"

    def has_permission(self, request, view):
        """By default, headers key are been changed from
                LEADBOARD_SK_HEADER to Leadboard-Sk-Header that's why we change the key """
        # check first  if the user is not authenticated
        if not request.user.is_authenticated:
            return False
        for key, value in request.headers.items():
            #  check the host if we are running manage.py test and if it's on test
            #  mode we allow without the headers .
            #  Note if we pass in headers it provides errors with throttle_scope
            if request.get_host() == "testserver":
                return True
            if key.lower() == 'leadboard-sk-header':
                leadboard_sk_header = request.headers['Leadboard-Sk-Header']
                is_header = leadboard_sk_header == config('LEADBOARD_SK_HEADER')
                return is_header


class LoggedInStaffPermission(BasePermission):
    message = "You don't have permission you must be a staff user"

    def has_permission(self, request, view):
        """By default, headers key are been changed from
                LEADBOARD_SK_HEADER to Leadboard-Sk-Header that's why we change the key """
        #  if the user is not authenticated
        if not request.user.is_authenticated:
            return False
        for key, value in request.headers.items():
            #  check the host if we are running manage.py test and if it's on test
            #  mode we allow without the headers .
            #  Note if we pass in headers it provides errors with throttle_scope
            if request.get_host() == "testserver":
                return True
            if key.lower() == 'leadboard-sk-header':
                leadboard_sk_header = request.headers['Leadboard-Sk-Header']
                is_header = leadboard_sk_header == config('LEADBOARD_SK_HEADER')
                return is_header == request.user.is_staff


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

        for key, value in request.headers.items():
            #  check the host if we are running manage.py test and if it's on test
            #  mode we allow without the headers .
            #  Note if we pass in headers it provides errors with throttle_scope
            if request.get_host() == "testserver":
                return True
            if key.lower() == 'leadboard-sk-header':
                leadboard_sk_header = request.headers['Leadboard-Sk-Header']
                is_header = leadboard_sk_header == config('LEADBOARD_SK_HEADER')
                return bool(
                    request.method in SAFE_METHODS or
                    request.user and
                    request.user.is_authenticated and
                    is_header
                )
