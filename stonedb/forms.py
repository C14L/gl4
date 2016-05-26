from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms
from django.utils.translation import ugettext_lazy as _

from companydb.models import Pic


class StoneSearchByNameForm(forms.Form):
    q = forms.CharField(max_length=100, required=True, strip=True, label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_stone-pseu-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.layout = Layout(
            Field('q', placeholder=_('Search by stone name'),
                  autocomplete="off"))


class PicUploadForm(forms.ModelForm):
    pic = forms.ImageField()
    caption = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Pic
        fields = ['pic', 'caption']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_profile-upload-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'pic', 'caption',
            FormActions(
                Submit('save', _('Add picture')),
            )
        )
