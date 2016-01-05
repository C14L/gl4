from django import forms


class PicUploadForm(forms.Form):
    pic = forms.ImageField(label='Select a file')
    title = forms.CharField(max_length=200, required=False, label='Title',
                            help_text='A short title for the picture.')
    caption = forms.CharField(max_length=500, required=False, label='Caption',
                              widget=forms.Textarea,
                              help_text='Optionally, some more information '
                                        'about the picture.')
