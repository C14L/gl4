from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from crispy_forms.bootstrap import FormActions
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

from companydb.models import UserProfile, Pic, Project, Stock


class CompanyProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['description', ]

    def __init__(self, *args, **kwargs):
        super(CompanyProjectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id_company-project-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.layout = Layout(
            'description',

            FormActions(
                Submit('save', _('Submit')),
                # Button('cancel', _('Cancel'))
            )
        )


class CompanyStockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['stone', 'dim_type', 'dim_total', 'description']

    def __init__(self, *args, **kwargs):
        super(CompanyStockForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_company-stock-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'stone', 'dim_type', 'dim_total', 'description',

            FormActions(
                Submit('save', _('Submit')),
                # Button('cancel', _('Cancel'))
            )
        )


class CompanyAboutForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['about', ]

    def __init__(self, *args, **kwargs):
        super(CompanyAboutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_company-about-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'about',

            FormActions(
                Submit('save', _('Submit')),
                # Button('cancel', _('Cancel'))
            )
        )


class CompanyDetailsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'contact', 'contact_position',
                  'street', 'city', 'zip', 'country_sub_name', 'country_name',
                  'email', 'fax', 'tel', 'mobile', 'web', ]

    def __init__(self, *args, **kwargs):
        super(CompanyDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_company-details-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'name', 'contact', 'contact_position',
            'street', 'city', 'zip', 'country_sub_name', 'country_name',
            'email', 'fax', 'tel', 'mobile', 'web',

            FormActions(
                Submit('save', _('Submit')),
                # Button('cancel', _('Cancel'))
            )
        )


class PicUploadForm(forms.ModelForm):
    class Meta:
        model = Pic
        fields = ['title']

    pic = forms.ImageField(label='Select a file')
    # title = forms.CharField(
    #    max_length=200, required=False, label='Title',
    #    help_text='A short title for the picture.')
    # caption = forms.CharField(
    #    max_length=500, required=False, label='Caption', widget=forms.Textarea,
    #    help_text='Optionally, some more information about the picture.')

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
            'pic', 'title',  # 'caption',
            FormActions(
                Submit('save', _('Add picture')),
            )
        )


class CompanyContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, strip=True)
    email = forms.EmailField(max_length=100, required=True, strip=True)
    msg = forms.CharField(widget=forms.Textarea,
                          max_length=100000, required=True, strip=True)
    leave_this_empty = forms.CharField(label='leave empty',
                                       max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_profile-contact-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'leave_this_empty', 'name', 'email', 'msg',
            FormActions(
                Submit('send', _('Send message'))
            ))

    def clean_leave_this_empty(self):
        # Hidden honeypot field that only bots fill in.
        if self.cleaned_data['leave_this_empty']:
            raise ValidationError('Unexpected value found.')

        return ''
