from django.http import HttpResponseBadRequest


# custom decorator to check if incoming request is ajax or not
def ajax_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.is_aja():
            return HttpResponseBadRequest
        return func(request, *args, **kwargs)
    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    return wrapper