from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    # whenever users_like will be changed, it will trigger a signal
    # that signal will be recieved by this reciever and will change the total_likes acordingly
    instance.total_likes = instance.users_like.count()
    instance.save()
