from django.http import HttpResponseBadRequest


# custom decorator to check if incoming request is ajax or not
def ajax_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest
        return func(request, *args, **kwargs)
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper
