import os
import json

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test

from .image import resize
from .forms import FileForm
from .settings import PREPEND_MEDIA_URL, UPLOAD_PATH


def _handle_upload(file_, upload_to, return_type_icon=True, result_image=None):
    """
    Handle image upload.
    Returns a JSON encoded response with 'url' (image thumbnail  URL) and
    'filename' (uploaded image path) attributes

    :param: request: request
    :param: upload_to: media subdirectory to upload image to
    """
    file_name, extension = os.path.splitext(file_.name)
    file_name = "".join([c for c in file_name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    safe_name = '{0}{1}'.format(file_name, extension)
    file_path = default_storage.save(os.path.join(upload_to or UPLOAD_PATH, safe_name), file_)
    file_url = os.path.join(settings.MEDIA_URL, file_path)

    if result_image:
        return_type_icon = False

    url = file_url
    if return_type_icon:
        root, ext = os.path.splitext(file_path)
        if (ext and
                os.path.exists(os.path.join(settings.STATIC_ROOT, 'ajaximage', 'img', "%s.png" % ext[1:]))):
                url = "%s/ajaximage/img/%s.png" % (settings.STATIC_URL, ext[1:])
        else:
            url = "%s/ajaximage/img/generic.png" % settings.STATIC_URL
    if result_image:
        url = result_image

    if PREPEND_MEDIA_URL:
        filename = file_url
    else:
        filename = file_path
    return url, filename


@csrf_exempt
@require_POST
def ajaximage(request, upload_to=None, max_width=None, max_height=None,
              crop=None, form_class=FileForm):
    """
    Handle image upload.
    Returns a JSON encoded response with 'url' (image thumbnail  URL) and
    'filename' (uploaded image path) attributes

    :param: request: request
    :param: upload_to: media subdirectory to upload image to
    :param: max_width: width to resize the image to
    :param: max_height: height to resize the image to
    :param: crop: whether cropping the image to the width / height constraints
    :param: form_class: stub form class to handle upload
    """
    form = form_class(request.POST, request.FILES)
    if form.is_valid():
        file_ = form.cleaned_data['file']
        image_types = ['image/png', 'image/jpg', 'image/jpeg', 'image/pjpeg', 'image/gif']
        if file_.content_type not in image_types:
            return HttpResponse(status=403, content='Bad image format')
        file_ = resize(file_, max_width, max_height, crop)
        url, filename = _handle_upload(file_, upload_to, False, form.result_image)

        return HttpResponse(json.dumps({'url': url, 'filename': filename}))
    return HttpResponse(status=403)


@csrf_exempt
@require_POST
def ajaxgeneric(request, upload_to=None, form_class=FileForm):
    """
    Handle generic files upload.
    Returns a JSON encoded response with 'url' (icon URL) and 'filename'
    (uploaded file path) attributes

    :param: request: request
    :param: upload_to: media subdirectory to upload image to
    :param: form_class: stub form class to handle upload
    :param: result_image: URL to the image to show as result (if given, overrides any other setting)
    """
    form = form_class(request.POST, request.FILES)
    if form.is_valid():
        url, filename = _handle_upload(form.cleaned_data['file'], upload_to, True, form.result_image)

        return HttpResponse(json.dumps({'url': url, 'filename': filename}))
    return HttpResponse(status=403)


@user_passes_test(lambda u: u.is_staff)
def ajaximage_auth(request, upload_to=None, max_width=None, max_height=None,
                   crop=None, form_class=FileForm):
    return ajaximage(request, upload_to, max_width, max_height, crop,
                     form_class)

@user_passes_test(lambda u: u.is_staff)
def ajaxgeneric_auth(request, upload_to=None, form_class=FileForm):
    return ajaxgeneric(request, upload_to, form_class)

@user_passes_test(lambda u: u.is_staff)
def ajaximage_staff(request, upload_to=None, max_width=None, max_height=None,
                    crop=None, form_class=FileForm):
    return ajaximage(request, upload_to, max_width, max_height, crop,
                     form_class)

@user_passes_test(lambda u: u.is_staff)
def ajaxgeneric_staff(request, upload_to=None, form_class=FileForm):
    return ajaxgeneric(request, upload_to, form_class)
