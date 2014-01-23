from django.utils.encoding import smart_text, force_unicode
import os
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


from .settings import PREPEND_MEDIA_URL

HTML_IMG = u"""
<div class="ajaximage" data-type="{type}" data-url="{upload_url}">
    <a class="link" target="_blank" href="{file_url}"><img src="{file_url}"></a>
    <a class="remove" href="#remove">{remove_label}</a>
    <input type="hidden" value="{file_path}" id="{element_id}" name="{name}" />
    <input type="file" class="fileinput" />
    <div class="progress progress-striped active">
        <div class="bar"></div>
    </div>
</div>
"""

HTML_TEXT = u"""
<div class="ajaximage" data-type="{type}" data-url="{upload_url}">
    <span class="text_file">{file_url}</span>
    <a class="remove" href="#remove">{remove_label}</a>
    <input type="hidden" value="{file_path}" id="{element_id}" name="{name}" />
    <input type="file" class="fileinput" />
    <div class="progress progress-striped active">
        <div class="bar"></div>
    </div>
</div>
"""


class AjaxFileEditor(widgets.TextInput):
    upload_url = 'ajaxfile'
    kwargs = {}
    type = 'file'
    template = HTML_TEXT
    remove_label = _(u'Remove')

    class Media:
        js = (
            'ajaximage/js/jquery-1.10.0.min.js',
            'ajaximage/js/jquery.iframe-transport.js',
            'ajaximage/js/jquery.ui.widget.js',
            'ajaximage/js/jquery.fileupload.js',
            'ajaximage/js/ajaximage.js',
        )
        css = {
            'all': (
                'ajaximage/css/bootstrap-progress.min.css',
                'ajaximage/css/styles.css',
            )
        }

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        self.show_icon = kwargs.pop('show_icon', False)
        self.kwargs = {'upload_to': self.upload_to}
        super(AjaxFileEditor, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        element_id = final_attrs.get('id')
        
        upload_url = reverse(self.upload_url, kwargs=self.kwargs)
        file_path = value if value else ''
        if PREPEND_MEDIA_URL is False and len(file_path) > 0:
            file_url = os.path.join(settings.MEDIA_URL, file_path)
        else:
            file_url = file_path

        file_name = os.path.basename(file_url)

        if self.show_icon:
            template = HTML_IMG
        else:
            template = self.template
        output = template.format(upload_url=upload_url,
                                 file_url=file_url,
                                 file_name=file_name,
                                 file_path=file_path,
                                 element_id=element_id,
                                 remove_label=force_unicode(self.remove_label),
                                 type=self.type,
                                 name=name)

        return mark_safe(unicode(output))


class AjaxImageEditor(AjaxFileEditor):
    upload_url = 'ajaximage'
    type = 'image'
    template = HTML_IMG

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        self.max_width = kwargs.pop('max_width', '')
        self.max_height = kwargs.pop('max_height', '')
        self.crop = kwargs.pop('crop', '')
        self.kwargs = {'upload_to': self.upload_to,
                       'max_width': self.max_width,
                       'max_height': self.max_height,
                       'crop': self.crop}
        super(AjaxFileEditor, self).__init__(*args, **kwargs)
