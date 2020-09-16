from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    def ready(self):
        """
            as soon as the app registry is fully populated,
            the receiver() decorator will register the signal reciever
        """
        import images.signals
