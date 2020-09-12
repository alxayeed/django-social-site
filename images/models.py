from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Image(models.Model):
    # in order to keep the code generic, refering to the User model using AUTH_USER_MODEL setting instead directly refering to it
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            blank=True)
    url = models.URLField()
    # images will be uploaded to the specified folder in MEDIA_URL
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,
                               db_index=True)

    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)

    # overriding the save() mathod to auto-generate the slug field based on the value of title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
