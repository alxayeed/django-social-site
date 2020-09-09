from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    This will allow additional feature to log in a user using email
    """

    # overriding authenticate() - to check aganst email and password
    def authenticate(self, request, username=None, password=None):

        try:
            user = User.objects.get(email=username)

            # checking password using User object method
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    # takes id/pk and return User object
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
