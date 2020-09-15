from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import ImageCreationForm
from .models import Image
from django.http import JsonResponse, HttpResponse
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action


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
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image has been sucessfully added')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # fill the form with the GET data that contains url and title
        form = ImageCreationForm(data=request.GET)

    return render(request, 'images/image/create.html',
                  {'section': 'images',
                   'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html',
                  {'section': 'images',
                   'image': image})


@ajax_required
@login_required
# allow only POST request, returns 405(HttpResponseNotAllowed) otherwise
@require_POST
def like_image(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                # adds only once if already exists
                image.users_like.add(request.user)
            else:
                # removes if exists, does nothing otherwise
                image.users_like.remove(request.user)
                create_action(request.user, 'likes', image)

            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


# view to list all bookmarked inages
@login_required
def image_list(request):
    images = Image.objects.all()
    # PAGINATOR
    paginator = Paginator(images, 6)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # First page
        images = paginator.page(1)
    except EmptyPage:
        # if page object is is out of range and
        if request.is_ajax():
            # if request is ajax, return empty page to stop ajax pagination on browser
            return HttpResponse('')
        # if page is out of range but request is not ajax, deliver last page
        images = paginator.page(paginator.num_pages)

    # if request is ajax, but not out of page, deliver ajax paginated list
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})

    # if not ajax request, deliver standard paginated list
    return render(request,
                  'images/image/list.html',
                  {'section': 'images', 'images': images})
