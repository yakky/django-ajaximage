#-*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import Field

from .widgets import AjaxImageEditor, AjaxFileEditor


class AjaxFileField(Field):
    result_image = None
    return_type_icon = False

    def __init__(self, *args, **kwargs):
        upload_to = kwargs.pop('upload_to', '')
        self.result_image = kwargs.pop('result_image', None)
        self.return_type_icon = kwargs.pop('return_type_icon', False)
        widget = kwargs.pop('widget', None)
        if widget:
            self.widget = widget(upload_to=upload_to,
                                 result_image=self.result_image)
        else:
            self.widget = AjaxFileEditor(upload_to=upload_to,
                                         result_image=self.result_image)
        super(AjaxFileField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)
        return super(AjaxFileField, self).formfield(**defaults)


class AjaxImageField(AjaxFileField):
    def __init__(self, *args, **kwargs):
        upload_to = kwargs.pop('upload_to', '')
        self.result_image = kwargs.pop('result_image', None)
        self.return_type_icon = kwargs.pop('return_type_icon', False)
        max_height = kwargs.pop('max_height', 0)
        max_width = kwargs.pop('max_width', 0)
        crop = kwargs.pop('crop', False)
        crop = 1 if crop is True else 0

        if crop is 1 and (max_height is 0 or max_width is 0):
            raise Exception(
                'Both max_width and max_height are needed if cropping')

        widget = kwargs.pop('widget', None)
        if widget:
            self.widget = widget(upload_to=upload_to, max_width=max_width,
                                 max_height=max_height, crop=crop)
        else:
            self.widget = AjaxImageEditor(upload_to=upload_to,
                                          max_width=max_width,
                                          max_height=max_height,
                                          crop=crop)

        super(AjaxImageField, self).__init__(*args, **kwargs)


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], ["^ajaximage\.fields\.AjaxFileField"])
    add_introspection_rules([], ["^ajaximage\.fields\.AjaxImageField"])
