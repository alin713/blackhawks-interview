import datetime
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic.base import TemplateView
from records.forms import (
    SearchForm,
    UserProfileForm,
)
from records.models import Client, Referral


class AttendanceReport(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    model = Client
    template_name = "records/reports/report-missed-class.html"
    permission_required = ("records.view_client", "records.view_service")

    def get_queryset(self):
        end = date.today()
        start = date.today() - datetime.timedelta(7)
        active_clients = Client.objects.filter(current_status="A", deleted=False)
        missed_class = [
            client for client in active_clients if not client.attended_class(start, end)
        ]
        return missed_class


def search_clients_advanced(contains=False, locations=(), status=(), **kwargs):
    client_list = Client.objects.filter(deleted=False)
    for key, value in kwargs.items():
        if value != "" and value is not None:
            if contains and isinstance(value, str):
                key = key + "__contains"
            client_list = client_list.filter(**{key: value})
    client_list = multi_filter(client_list, "primary_location", locations, contains)
    client_list = multi_filter(client_list, "current_status", status, contains)
    return client_list.order_by("l_name")


def multi_filter(client_list, field, field_list, contains):
    if contains:
        field = field + "__contains"
    if field_list:
        if len(field_list) > 0:
            new_list = client_list.filter(**{field: field_list[0]})
        else:
            new_list = client_list
        for index in range(1, len(field_list)):
            new_list = new_list | client_list.filter(**{field: field_list[index]})
        return new_list
    return client_list


def search_referrals_advanced(contains=False, **kwargs):
    ref_list = Referral.objects.filter(deleted=False)
    for key, value in kwargs.items():
        if value != "":
            if contains:
                key = key + "__contains"
            ref_list = ref_list.filter(**{key: value})
    return ref_list.order_by("agency")


class AdvancedSearch(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "records/search/search-advanced.html"
    permission_required = ("records.view_client", "records.view_referral")

    def get_context_data(self, **kwargs):
        context = super(AdvancedSearch, self).get_context_data(**kwargs)
        context["form"] = SearchForm()
        return context


class AdvancedSearchResults(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = "records/search/search-advanced-results.html"
    permission_required = ("records.view_client", "records.view_referral")
    client_results = None
    referral_results = None

    def post(self, request):
        if request.method == "POST":
            searchbar = request.POST.get("searchbar")
            if searchbar:
                name_list = searchbar.split()
                self.client_results = search_clients_advanced(
                    True, f_name=name_list[0]
                ) | search_clients_advanced(True, l_name=name_list[0])
                for name in name_list[1:]:
                    self.client_results = (
                        self.client_results
                        | search_clients_advanced(True, f_name=name)
                        | search_clients_advanced(True, l_name=name)
                    )
            else:
                form = SearchForm(request.POST)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    contains = request.POST.get("contains", False)
                    dcs_status = request.POST.get("dcs", False)
                    if dcs_status == "on":
                        dcs_status = True
                    else:
                        dcs_status = None
                    if cleaned_data["search_type"] == "Clients":
                        self.client_results = search_clients_advanced(
                            contains,
                            locations=cleaned_data["locations"],
                            status=cleaned_data["status"],
                            f_name=cleaned_data["f_name"],
                            l_name=cleaned_data["l_name"],
                            phone=cleaned_data["phone"],
                            email=cleaned_data["email"],
                            dcs=dcs_status,
                        )
                    else:
                        self.referral_results = search_referrals_advanced(
                            contains,
                            full_name=cleaned_data["full_name"],
                            agency=cleaned_data["agency"],
                            phone=cleaned_data["ref_phone"],
                            email=cleaned_data["ref_email"],
                        )
                    return self.render_to_response(
                        self.get_context_data(
                            phone=cleaned_data["phone"],
                            email=cleaned_data["email"],
                            dcs=dcs_status,
                            ref_phone=cleaned_data["ref_phone"],
                            ref_email=cleaned_data["ref_email"],
                        )
                    )
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(AdvancedSearchResults, self).get_context_data(**kwargs)
        context["clients"] = self.client_results
        context["referrals"] = self.referral_results
        for key in kwargs:
            context[key] = kwargs[key]

        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "records/user/edit-profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["form"] = UserProfileForm(
            initial={
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
                "email": self.request.user.email,
            }
        )
        context["form_submit"] = "Save"
        return context


def save_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            for key in iter(cleaned_data):
                if not cleaned_data[key]:
                    if getattr(User, key).field.null:
                        cleaned_data[key] = None

            request.user.first_name = cleaned_data["first_name"]
            request.user.last_name = cleaned_data["last_name"]
            request.user.email = cleaned_data["email"]
            request.user.save()

    return HttpResponseRedirect(
        reverse(
            "records:edit-profile",
        )
    )
