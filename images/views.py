from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreationForm


@login_required
def create_image(request):
    if request.method == 'POST':
        form = ImageCreationForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # save the data and image in the object, but in the database
            new_item = form.save(commit=False)
            # add current user to the user of this item
            new_item.user = request.user
            # now save to db
            new_item.save()
            messages.success(request, 'Image has benn sucessfully added')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # fill the form with the GET data (url,title)
        form = ImageCreationForm(data=request.POST)

    return render(request, 'images/image/create.html',
                  {'section': 'images',
                   'form': form})
