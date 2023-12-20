from django.urls import path
from records.viewgroups import client_views, notes_views, other_views, print_views, referral_views, service_views

app_name = 'records'

# Client Views
client = [
    path('', client_views.IndexView.as_view(), name='index'),
    path('new/', client_views.ClientView.as_view(), name='client-new'),
    path('new/save/', client_views.add_client, name='client-add'),
    path('<int:pk>/', client_views.DetailView.as_view(), name='detail'),
    path('<int:pk>/email-link/', client_views.email_secure_link, name='email-secure-link'),
    path('<int:client_id>/<int:referral_id>/email-enrollment/', client_views.email_enrollment_to_referral, name='email-enrollment'),
    path('csr/<uuid:uuid>/<str:passcode>/', client_views.SecureLinkDetailView.as_view(), name='secure-detail'),
    path('<int:pk>/edit/', client_views.ClientEditView.as_view(), name='client-edit-view'),
    path('<int:client_id>/edit/save/', client_views.edit_client, name='client-edit'),
]

# Service Views
service = [
    path('service/<int:pk>/', service_views.ServiceView.as_view(), name='service'),
    path('service/<int:service_id>/edit/', service_views.edit, name='service-edit'),
    path('service/<int:service_id>/delete/', service_views.delete, name='service-del'),
    path('<int:client_id>/add/', service_views.add, name='add'),
]

# Casenote Views
notes = [
    path('<int:pk>/notes/', notes_views.NotesView.as_view(), name='notes'),
    path('<int:pk>/notes/print/', notes_views.NotesViewPrint.as_view(), name='notes-print'),
    path('<int:pk>/notes/print/select/', notes_views.NotesPrintSelect.as_view(), name='notes-print-select'),
    path('note/<int:pk>/', notes_views.CaseNoteView.as_view(), name='note'),
    path('<int:client_id>/notes/add/', notes_views.add_case_note, name='note-add'),
    path('note/<int:casenote_id>/edit/', notes_views.editCaseNote, name='note-edit'),
    path('note/<int:casenote_id>/delete/', notes_views.deleteCaseNote, name='note-del'),
]

# Referral Views
referral = [
    path("referral/", referral_views.ReferralView.as_view(), name="referral"),
    path("referral/<int:pk>/", referral_views.RefDetailView.as_view(), name="ref_detail"),
    path("referral/add/", referral_views.AddRefView.as_view(), name="add_ref"),
    path("referral/add/save/", referral_views.add_ref, name="save_ref"),
    path("referral/<int:pk>/edit/", referral_views.EditRefView.as_view(), name="edit_ref"),
    path("referral/<int:referral_id>/edit/save/", referral_views.edit_ref, name="edit_save_ref"),
    path("referral/<int:referral_id>/delete/", referral_views.delete_ref, name="delete_ref"),
    path("referral/<int:pk>/add-client/", referral_views.RefAddClient.as_view(), name="ref-add-client"),
    path("referral/<int:pk>/add-client/save/", referral_views.ref_save_client, name="ref-save-client"),
    path("referral/<int:pk>/delete-client/", referral_views.RefDelClient.as_view(), name="ref-del-client"),
    path('referral/<int:referral_id>/delete-client/<int:client_id>/', referral_views.client_del_ref, name='client-delete-ref'),
    path("referral/<int:pk>/delete-client-save/", referral_views.ref_del_client, name="ref-del-client-save"),
    path("referral/<int:pk>/add-multi-client/save/", referral_views.ref_save_multi_client, name="ref-save-multi-client"),
    path("referral/<int:pk>/del-multi-client/save/", referral_views.ref_del_multi_client, name="ref-save-del-multi-client"),
]

# Print Layout Views
print = [
    path('csr/<uuid:uuid>/<str:passcode>/print/pdf/', print_views.render_secure_pdf_csr, name='secure-detail-print-pdf'),
    path('<int:pk>/print/', print_views.DetailViewPrint.as_view(), name='detail-print'),
    path('<int:pk>/print/pdf/', print_views.render_pdf_csr, name='detail-print-pdf'),
    path('<int:pk>/notes/print/pdf/', print_views.render_pdf_gs, name='notes-print-pdf'),
]

# Reporting
reports = [
    path("report/attendance/", other_views.AttendanceReport.as_view(), name="attendance"),
]

# Search bar
search = [
    path("advanced-search/", other_views.AdvancedSearch.as_view(), name="advanced-search"),
    path("advanced-search/results/", other_views.AdvancedSearchResults.as_view(), name="advanced-search-results"),
]

# User Profiles
user = [
    path('profile/', other_views.ProfileView.as_view(), name='edit-profile'),
    path('profile/save/', other_views.save_profile, name='save-profile'),
]

urlpatterns = [
    client,
    service,
    notes,
    referral,
    print,
    search,
    user,
    reports,
]
urlpatterns = [url for group in urlpatterns for url in group]