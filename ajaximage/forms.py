from django import forms


class FileForm(forms.Form):
    # Image to return after successful upload (if empty the uploaded image or a default icon is used)
    result_image = None

    file = forms.FileField()