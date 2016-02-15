from crispy_forms.bootstrap import FormActions
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout

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
                Submit('save', 'Submit'),
                # Button('cancel', 'Cancel')
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
        self.helper.form_action = 'companydb_db_stock'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'stone', 'dim_type', 'dim_total', 'description',

            FormActions(
                Submit('save', 'Submit'),
                # Button('cancel', 'Cancel')
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
        self.helper.form_action = 'companydb_db_about'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'about',

            FormActions(
                Submit('save', 'Submit'),
                # Button('cancel', 'Cancel')
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
        self.helper.form_action = 'companydb_db_details'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'name', 'contact', 'contact_position',
            'street', 'city', 'zip', 'country_sub_name', 'country_name',
            'email', 'fax', 'tel', 'mobile', 'web',

            FormActions(
                Submit('save', 'Submit'),
                # Button('cancel', 'Cancel')
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
        super(PicUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_profile-upload-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'companydb_db_pics'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'pic', 'title',  # 'caption',
            FormActions(
                Submit('save', 'Add picture'),
            )
        )
