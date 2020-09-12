from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreationForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description', 'url')
        widgets = {
            'url': forms.HiddenInput
        }

    # clean method for url to check whether it allows only JPG/JPEG or not(ends with .jpg or .jpeg)
    # this method will be executed on is_valid() call
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        # splitting once where a . is found, taking the [1]( second ) split, and make it lowercase
        extension = url.rsplit('.', 1)[1].lower()

        if extension not in valid_extensions:
            raise forms.ValidationError(
                'The given url does not match with valid image extensions')
        return url

    # overriding save() method to save the image when this method is called
    def save(self, force_insert=False,
             force_update=False,
             commit=True):

        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(self.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # download image from the url
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()),
                         save=False)
        if commit:
            image.save()
        return image
