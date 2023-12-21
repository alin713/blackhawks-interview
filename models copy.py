import datetime
import secrets
import string
import uuid


from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Maximum CharField lengths
MAX_EMAIL = 64
MAX_NAME = 32
MAX_PHONE = 22

LOCATIONS = sorted(
    [
        "Lafayette",
        "Anderson",
        "Bloomington",
        "Crawfordsville",
        "Delphi",
        "Elwood",
        "Evansville",
        "Muncie",
        "Rennselaer",
        "Terre Haute",
        "Vincennes",
        "Indianapolis/Franklin",
        "Virtual",
    ]
)
LOCATIONS.append("No City Chosen")
LOCATION_CHOICES = [tuple([location, location]) for location in LOCATIONS]

SERVICES = [
    "Attended Class Session",
    "Attended Class Session-Zoom",
    "DCS Attended Class",
    "DCS Attended Class-Zoom",
    "0 Absences Remaining",
    "1 Absence Remaining",
    "2 Absences Remaining ",
    "Absence Excused By Program Director",
    "Absence Excused",
    "Absent From Class",
    "Active Status Reinstated",
    "Admin File Review",
    "DV Assessment",
    "Attended Extra Class",
    "Attended Free Class",
    "Attended Intake Orientation",
    "Bad Check Fee",
    "Class Cancelled this Week",
    "Completed Program",
    "Complied with Referral Source Requirements",
    "Convenience Fee",
    "Court Appearance Subpoenaed",
    "Co-Facilitated Class Session",
    "DCS Court Appearance Subpoenaed",
    "DCS FCM Team Meeting",
    "DCS Individual Session",
    "DCS Intake Orientation 1.0 Hour",
    "DCS Non Credit Class Arrived Late ",
    "DCS Non Credit Class Left Early ",
    "DCS Non Credit Class Rule Violation",
    "DCS Referral Ended / Withdrawn",
    "Error",
    "Emailed Participant",
    "Excused Absence Court",
    "Excused Absence Incarcerated",
    "Excused Absence Medical",
    "Excused Absence Military Duty",
    "Facilitated Class Session",
    "Individual Office Discussion",
    "Late Fee",
    "No Show- Client Never Enrolled",
    "No Show - Scheduled Appointment",
    "Non Credit - Arrived Late",
    "Non Credit - Came to Office Intoxicated",
    "Non Credit - Deferred",
    "Non Credit - Left Early",
    "Non Credit - Program Rule Violated",
    "Non Credit - Short 12 Step Reports",
    "Non Credit- Disruptive Behavior in Class",
    "Non Credit-Zoom",
    "Observed Class ",
    "Other (specify)",
    "Payment - No Session Attended",
    "Payment Refund",
    "Previous Balance Brought Forward",
    "Program Extended",
    "Received New Referral",
    "Received Notebook",
    "Refused to Attend Intake Orientation",
    "Refused to Sign Enrollment Agreement",
    "Returned Check Fee",
    "Scheduled Appointment",
    "Telephone Discussion",
    "Telephone Message Left",
    "Threatened Suicide 911 Notified",
    "Transferred From Another Program",
    "Transferred to Another Program",
    "Texts/ Emails Sent to Client",
    "Texts/Emails Sent to Referral Source",
    "Text/Email Received from Client",
    "Unable to Contact Client",
    "Unbillable Team Meeting",
    "Violated Abusive Behavior Instructed to Leave",
    "Violated Admitted Alcohol or Drug Use",
    "Violated Disruptive Behavior in Class",
    "Violated Excessive Absences",
    "Violated New Abuse Allegations",
    "Violated New Criminal Charge",
    "Violated Positive Alcohol/Drug Test",
    "Violated Program Rules",
    "Violated Quit Attending",
    "Violated Refused to Comply with Staff",
    "Violated Rules - Abuse Outside of Class",
    "Volunteer Work Credit",
    "Waiting for Client to Come and Enroll",
]
SERVICE_CHOICES = [tuple([service, service]) for service in SERVICES]

FEES = [0.00, 2.00, 4.00, 8.00, 25.00, 30.00, 35.00, 40.00]
FEE_CHOICES = [tuple([f"{fee:.2f}", f"{fee:.2f}"]) for fee in FEES]

DISCOUNTS = [0.00, 5.00, 10.00, 15.00, 20.00, 25.00, 30.00, 35.00, 40.00]
DISCOUNT_CHOICES = [tuple([f"{discount:.2f}", f"{discount:.2f}"]) for discount in DISCOUNTS]

ETHNICITIES = [
    "White",
    "Black or African-American",
    "Latino or Hispanic",
    "American Indian or Alaskan Native",
    "Asian",
    "Native Hawaiian or other Pacific Islander",
    "Two or more",
    "Prefer not to say",
]
ETHNICITY_CHOICES = [tuple([ethnicity, ethnicity]) for ethnicity in ETHNICITIES]

GENDERS = ["Male", "Female", "Non-binary", "Prefer not to say"]
GENDER_CHOICES = [tuple([gender, gender]) for gender in GENDERS]

LANGUAGES = [
    "English",
    "Spanish",
    "Chinese",
    "French",
    "Some other language",
    "Prefer not to say",
]
LANGUAGE_CHOICES = [tuple([language, language]) for language in LANGUAGES]

RELATIONSHIPS = ["Married", "Single", "In a relationship", "Prefer not to say"]
RELATIONSHIP_CHOICES = [
    tuple([relationship, relationship]) for relationship in RELATIONSHIPS
]

EMPLOYMENTS = [
    "Employed Full-time",
    "Employed Part-time",
    "Not Employed",
    "Retired",
    "Disabled or Unable to work",
    "Prefer not to say",
]
EMPLOYMENT_CHOICES = [tuple([employment, employment]) for employment in EMPLOYMENTS]

ACTIVE = "A"
PENDING = "P"
UNSUCCESSFUL = "U"
SUCCESSFUL = "S"
INACTIVE = "I"

CURRENT_STATUS_CHOICES = [
    (ACTIVE, "Active"),
    (PENDING, "Pending"),
    (UNSUCCESSFUL, "Unsuccessful"),
    (SUCCESSFUL, "Successful"),
    (INACTIVE, "Inactive"),
]


def generate_passcode():
    return "".join(
        secrets.choice(string.ascii_letters + string.digits) for i in range(6)
    )


class Client(models.Model):
    class Meta:
        permissions = [
            ("lafayette", "Can see clients from Lafayette"),
            ("all_clients", "Can see all clients regardless of location"),
        ]

    # Client Personal/Case/Program Information
    f_name = models.CharField("First Name", max_length=MAX_NAME)  # Required
    m_name = models.CharField("Middle Name", max_length=MAX_NAME, blank=True)
    l_name = models.CharField("Last Name", max_length=MAX_NAME)  # Required
    phone = models.CharField("Phone Number", max_length=MAX_PHONE, blank=True)
    email = models.CharField("Email", max_length=MAX_EMAIL, blank=True)
    dcs = models.BooleanField("DCS Client", null=True)

    primary_location = models.CharField(
        "Primary Location",
        max_length=50,
        blank=True,
        choices=LOCATION_CHOICES,
        default="No City Chosen",
    )

    dob = models.DateField("Date of Birth", blank=True, null=True)
    ethnicity = models.CharField(
        "Ethnicity", blank=True, max_length=50, choices=ETHNICITY_CHOICES
    )
    gender = models.CharField(
        "Gender", blank=True, max_length=50, choices=GENDER_CHOICES
    )
    language = models.CharField(
        "Language", blank=True, max_length=50, choices=LANGUAGE_CHOICES
    )
    relationship_status = models.CharField(
        "Relationship Status", blank=True, max_length=50, choices=RELATIONSHIP_CHOICES
    )
    employment_status = models.CharField(
        "Employment Status", blank=True, max_length=50, choices=EMPLOYMENT_CHOICES
    )

    # Cause Numbers (up to 3)
    cause = models.CharField("Cause Number", max_length=25, blank=True)
    cause2 = models.CharField("Cause Number 2", max_length=25, blank=True)
    cause3 = models.CharField("Cause Number 3", max_length=25, blank=True)

    date_enroll = models.DateField("Date Enrolled", null=True, blank=True)
    date_discharge = models.DateField("Date Discharged", null=True, blank=True)
    date_complete = models.DateField("Date Completed", null=True, blank=True)

    # Track when changes occur and who made them
    last_updated = models.DateTimeField("Last Updated", auto_now=True)
    last_updated_by = models.CharField(
        "Last Updated By", max_length=MAX_NAME * 2, default="System", blank=True
    )

    # Implementing the deletion model
    deleted = models.BooleanField("Deleted", default=False)
    deleted_on = models.DateTimeField("Deleted On:", blank=True, null=True)
    deleted_by = models.CharField("Deleted By:", max_length=MAX_NAME * 2, blank=True)

    LONG = 40
    SHORT = 26
    SESSION_QTY_CHOICES = [
        (LONG, "40 weeks"),
        (SHORT, "26 weeks"),
    ]
    sesh_qty_orig = models.SmallIntegerField(
        "Original Required Sessions to Complete",
        choices=SESSION_QTY_CHOICES,
        default=LONG,
    )
    session_qty_add = models.SmallIntegerField(
        "Additional Sessions Assigned While in the Program",
        default=0,
    )

    current_status = models.CharField(
        "Current Status",
        max_length=1,
        choices=CURRENT_STATUS_CHOICES,
        default=PENDING,
    )

    # UUID, Passcode, and other fields for "Secure Link" feature
    uuid = models.UUIDField("UUID", default=uuid.uuid4)
    passcode = models.CharField("Passcode", max_length=6, default=generate_passcode)
    link_access_timout = models.DateTimeField(
        "Link Access Timeout", default=timezone.now
    )

    # Client methods
    def __str__(self):
        if self.m_name:
            return f"{self.f_name} {self.m_name} {self.l_name}".title()
        else:
            return f"{self.f_name} {self.l_name}".title()

    @admin.display(
        boolean=False,
        description="Sessions Remaining",
    )
    def credits(self):
        """Computes the total credit a client has earned"""
        services = Service.objects.filter(client=self.pk, deleted=False)
        credits = 0
        for service in services:
            if service.credit is not None and not 0:
                credits += service.credit
        sessions_left = credits
        return sessions_left

    def payments(self):
        """Computers the total amount a client has payed"""
        services = Service.objects.filter(client=self.pk, deleted=False)
        payments = 0
        for service in services:
            if service.payment is not None and not 0:
                payments += service.payment
        return payments

    def fees(self):
        """Computes the total amount a client owes in fees"""
        services = Service.objects.filter(client=self.pk, deleted=False)
        fees = 0
        for service in services:
            if service.fee is not None and not 0:
                fees += service.fee
        return fees

    def discounts(self):
        """Computer the total amount of discounts a client has received"""
        services = Service.objects.filter(client=self.pk, deleted=False)
        discounts = 0
        for service in services:
            if service.discount is not None and not 0:
                discounts += service.discount
        return discounts

    def sessions_left(self):
        services = Service.objects.filter(client=self.pk, deleted=False)
        credits = 0
        for service in services:
            if service.credit is not None:
                credits += service.credit
        sessions_left = (self.sesh_qty_orig + self.session_qty_add) - credits
        return sessions_left

    def balance_remaining(self):
        services = Service.objects.filter(client=self.pk, deleted=False)
        fees = 0
        discounts = 0
        payments = 0
        balance = 0
        for service in services:
            if service.fee is not None:
                fees += service.fee
            if service.discount is not None:
                discounts += service.discount
            if service.payment is not None:
                payments += service.payment
        balance = (discounts + payments) - fees
        # return f'{balance:.2f}'
        return balance

    def attended_class(self, start_date, end_date):
        classes_attended = self.service_set.filter(
            desc__contains="Attended Class", date__range=(start_date, end_date)
        ) | self.service_set.filter(
            desc__contains="Deferred", date__range=(start_date, end_date)
        )
        if classes_attended.count() > 0:
            return True
        else:
            return False


class Service(models.Model):
    # Services and events that make up a Client Status Report. Foreign Key = Client
    """
    Backend Validators:
        date : required, sets default value
    Frontend Validators:
        date : required, sets default value
        desc : required
        fee : set choices
        discount : set choices
        credit : max
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField("Date", default="2000-01-01")
    desc = models.CharField("Description of Service", max_length=100, blank=True)
    fee = models.DecimalField(
        "Fee",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0, "Error: Enter positive numbers only")],
        # choices=FEE_CHOICES,
    )
    discount = models.DecimalField(
        "Discount",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0, "Error: Enter positive numbers only")],
        # choices=DISCOUNT_CHOICES,
    )
    payment = models.DecimalField(
        "Payment",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0, "Error: Enter positive numbers only")],
    )
    credit = models.PositiveSmallIntegerField("Credit", blank=True, null=True)
    notes = models.TextField("Notes", max_length=200, blank=True)

    # Track when changes occur and who made them
    last_updated = models.DateTimeField("Last Updated", auto_now=True)
    last_updated_by = models.CharField(
        "Last Updated By", max_length=MAX_NAME * 2, default="System", blank=True
    )

    # Implementing the deletion model
    deleted = models.BooleanField("Deleted", default=False)
    deleted_on = models.DateTimeField("Deleted On:", blank=True, null=True)
    deleted_by = models.CharField("Deleted By:", max_length=MAX_NAME * 2, blank=True)

    # Service methods
    def __str__(self):
        return f"{self.client.__str__()}-{self.desc}-{self.date}"

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)  # Call the "real" save() method.
        except ValidationError as e:
            print(e)

    def is_recent_activity(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.date <= now


class CaseNote(models.Model):
    # Case note entries that make up a Green Sheet. Foreign Key = Client
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField("Date")
    start_time = models.TimeField("Start Time", null=True)
    end_time = models.TimeField("End Time", null=True)
    facilitator = models.CharField("Facilitator", max_length=25)
    class_topic = models.CharField("Class Topic", max_length=25)
    notes = models.TextField("Notes", max_length=200, blank=True)
    location = models.CharField(
        "Location",
        max_length=50,
        blank=True,
        choices=LOCATION_CHOICES,
        default="No City Chosen",
    )

    # Track when changes occur and who made them
    last_updated = models.DateTimeField("Last Updated", auto_now=True)
    last_updated_by = models.CharField(
        "Last Updated By", max_length=MAX_NAME * 2, default="System", blank=True
    )

    # Implementing the deletion model
    deleted = models.BooleanField("Deleted", default=False)
    deleted_on = models.DateTimeField("Deleted On:", blank=True, null=True)
    deleted_by = models.CharField("Deleted By:", max_length=MAX_NAME * 2, blank=True)

    # CaseNote methods
    def __str__(self):
        return f"{self.client.__str__()}-{self.date}-{self.class_topic}"

    def save(self, *args, **kwargs):
        try:
            # Only validate start/end times when they are both present
            if self.start_time and self.end_time:
                self.validate_class_times()
            super().save(*args, **kwargs)  # Call the "real" save() method.
        except ValidationError as e:
            print(e)

    def validate_class_times(self):
        if self.start_time > self.end_time:
            raise ValidationError("Start time is after end time.")


class Referral(models.Model):
    clients = models.ManyToManyField(Client)
    full_name = models.CharField("Referred by", max_length=MAX_NAME * 2)
    agency = models.CharField("Agency", max_length=50)
    phone = models.CharField("Phone Number", max_length=MAX_PHONE, blank=True)
    email = models.CharField("Email", max_length=MAX_EMAIL, blank=True)

    # Track when changes occur and who made them
    last_updated = models.DateTimeField("Last Updated", auto_now=True)
    last_updated_by = models.CharField(
        "Last Updated By", max_length=MAX_NAME * 2, default="System", blank=True
    )

    # Implementing the deletion model
    deleted = models.BooleanField("Deleted", default=False)
    deleted_on = models.DateTimeField("Deleted On:", blank=True, null=True)
    deleted_by = models.CharField("Deleted By:", max_length=MAX_NAME * 2, blank=True)

    def __str__(self):
        return self.agency
