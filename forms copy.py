from django import forms
from django.forms import ModelForm, TimeInput, DateInput
from datetime import date, time, datetime

import records.models
from records.models import (
    Service,
    Client,
    CaseNote,
    Referral,
    SERVICE_CHOICES,
    LOCATION_CHOICES,
    MAX_EMAIL,
    MAX_NAME,
    MAX_PHONE,
    CURRENT_STATUS_CHOICES,
    FEE_CHOICES,
    DISCOUNT_CHOICES,
)
from django.contrib.auth.models import User


class ServiceForm(ModelForm):
    """This form basically mimics the Service Model except with more validation on the inputs"""

    class Meta:
        model = Service
        fields = "__all__"
        exclude = ["client", "last_updated_by", "last_updated"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": "2", "cols": "40"}),
            "credit": forms.NumberInput(
                attrs={"max": 1}
            ),  # ENFORCE: Max credit given is 1
        }

    # ENFORCE: (1) Date and desc are required (2) desc, fee and discount choices limited
    date = forms.DateField(
        label="Date",
        required=True,
        widget=DateInput(attrs={"type": "date", "value": date.today()}),
    )
    desc = forms.ChoiceField(
        label="Description of Service", required=True, choices=SERVICE_CHOICES
    )
    fee = forms.ChoiceField(label="Fee", choices=FEE_CHOICES)
    discount = forms.ChoiceField(label="Discount", choices=DISCOUNT_CHOICES)

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.template_name_div = "forms/div.html"
        self.template_name_label = "forms/label.html"
        for field in self.fields:
            # Add Bootstrap friendly classes to HTML inputs
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
        exclude = [
            "last_updated",
            "last_updated_by",
            "date_complete",
            # "dob",
            # "ethnicity",
            # "gender",
            # "language",
            # "relationship_status",
            # "employment_status",
            "uuid",
            "passcode",
            "link_access_timout",
        ]
        widgets = {
            "date_enroll": DateInput(attrs={"type": "date"}),
            "date_discharge": DateInput(attrs={"type": "date"}),
            "dob": DateInput(attrs={"type": "date"}),
        }
        labels = {
            "dcs": "DCS",
            "sesh_qty_orig": "Sessions Required",
            "session_qty_add": "Extra Sessions",
        }

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.template_name_label = "forms/label.html"
        # self.fields["sesh_qty_orig"].name = "Sessions Required"


class CaseNoteForm(ModelForm):
    class Meta:
        model = CaseNote
        fields = "__all__"
        exclude = ["client", "last_updated_by", "last_updated"]
        widgets = {
            # "date": DateInput(attrs={"type": "date"}),
            # "start_time": TimeInput(attrs={"type": "time", "step": 60}),
            # "end_time": TimeInput(attrs={"type": "time", "step": 60}),
            "notes": forms.Textarea(attrs={"rows": "2", "cols": "40"}),
        }

    # ENFORCE: (1) date, start_time, end_time, facilitator, and class_topic are required
    date = forms.DateField(
        label="Date",
        required=True,
        widget=DateInput(attrs={"type": "date", "value": date.today()}),
    )
    start_time = forms.TimeField(
        label="Start Time",
        required=True,
        widget=TimeInput(attrs={"type": "time", "step": 60}),
    )
    end_time = forms.TimeField(
        label="EndTime",
        required=True,
        widget=TimeInput(attrs={"type": "time", "step": 60}),
    )
    facilitator = forms.CharField(label="Facilitator", required=True)
    class_topic = forms.CharField(label="Class Topic", required=True)

    def __init__(self, *args, **kwargs):
        super(CaseNoteForm, self).__init__(*args, **kwargs)
        self.template_name_div = "forms/div.html"
        self.template_name_label = "forms/label.html"
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ReferralForm(ModelForm):
    class Meta:
        model = Referral
        fields = "__all__"
        exclude = ["clients", "last_updated", "last_updated_by"]

    def __init__(self, *args, **kwargs):
        super(ReferralForm, self).__init__(*args, **kwargs)
        self.template_name_div = "forms/div.html"
        self.template_name_label = "forms/label.html"
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ReferralClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ["f_name", "l_name", "email"]

    def __init__(self, *args, **kwargs):
        super(ReferralClientForm, self).__init__(*args, **kwargs)
        self.template_name_div = "forms/div.html"
        self.template_name_label = "forms/label.html"
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class SearchForm(forms.Form):
    search_type = forms.ChoiceField(
        label="Search Type",
        choices=(("Clients", "Clients"), ("Referrals", "Referrals")),
        required=True,
    )
    f_name = forms.CharField(label="First Name", max_length=MAX_NAME, required=False)
    l_name = forms.CharField(label="Last Name", max_length=MAX_NAME, required=False)
    phone = forms.CharField(label="Phone", max_length=MAX_PHONE, required=False)
    email = forms.CharField(label="Email", max_length=MAX_EMAIL, required=False)
    locations = forms.MultipleChoiceField(
        label="Locations",
        required=False,
        choices=LOCATION_CHOICES,
        help_text="Press CTRL or ⌘ while clicking to unselect",
    )
    status = forms.MultipleChoiceField(
        label="Status", choices=CURRENT_STATUS_CHOICES, required=False
    )
    full_name = forms.CharField(
        label="Full Name", max_length=MAX_NAME * 2, required=False
    )
    agency = forms.CharField(label="Agency", max_length=50, required=False)
    ref_phone = forms.CharField(label="Phone", max_length=MAX_PHONE, required=False)
    ref_email = forms.CharField(label="Email", max_length=MAX_EMAIL, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.template_name_div = "forms/div.html"
        self.template_name_label = "forms/label.html"
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class ReferralSelectForm(forms.Form):
    # ref_choices.insert(0, ('', ''))
    full_name = forms.ChoiceField(label="Referral Name", required=False)

    def __init__(self, *args, **kwargs):
        super(ReferralSelectForm, self).__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update({"class": "form-control"})
        ref_choices = [
            tuple(
                [self.get_referral_string(referral), self.get_referral_string(referral)]
            )
            for referral in Referral.objects.all()
        ]
        ref_choices.insert(0, ("", ""))
        self.fields["full_name"].choices = ref_choices

    def get_referral_string(self, referral):
        return f"{referral.agency}--{referral.full_name}"


class YearMonthForm(forms.Form):
    help_text = "You must enter a month or year if Full Report is not checked"
    month = forms.IntegerField(
        max_value=12, min_value=1, required=False, help_text=help_text
    )
    year = forms.IntegerField(max_value=2023, min_value=2022, required=False)
    all_time = forms.BooleanField(label="Full Report", required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super(YearMonthForm, self).__init__(*args, **kwargs)
        self.template_name_div = "forms/div.html"
        self.template_name_label = "forms/label.html"
        self.fields["month"].widget.attrs.update({"class": "form-control"})
        self.fields["year"].widget.attrs.update({"class": "form-control"})


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.template_name_div = "forms/div.html"
        self.template_name_label = "forms/label.html"
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class RefMultiClientForm(forms.Form):
    def __init__(self, *args, **kwargs):
        client_choices = kwargs.get("client_choices")
        if client_choices:
            del kwargs["client_choices"]
        super(RefMultiClientForm, self).__init__(*args, **kwargs)
        self.template_name_div = "forms/div.html"
        self.fields["clients"] = forms.ChoiceField(label="Clients Found")
        if client_choices:
            self.fields["clients"].choices = [
                tuple([client.id, self.get_client_string(client)])
                for client in client_choices
            ]
        else:
            # this is so that a form error is not thrown because there are no available choices when calling RefMultiClientForm(request.POST)
            # this makes it so that all the clients in the database are valid choices
            self.fields["clients"].choices = [
                tuple([client.id, self.get_client_string(client)])
                for client in Client.objects.all()
            ]
        self.fields["clients"].widget.attrs.update({"class": "form-control"})

    # this function changes what is displayed in the dropdown menu
    def get_client_string(self, client):
        display_str = f"{client}, "

        if client.email:
            display_str += f"{client.email}, "
        else:
            display_str += "No Email, "

        if client.phone:
            display_str += f"{client.phone}, "
        else:
            display_str += "No Phone, "

        display_str += f"City: {client.primary_location}, Status: {client.get_current_status_display()}"

        if client.dcs:
            display_str += ", DCS"

        return display_str
