from django.conf.urls import url

from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

from .views import PatientCreateView, PatientListView, PatientUpdateView, PatientDetailView
from .views import LocationCreateView, LocationListView, LocationUpdateView, LocationDetailView
from .views import ConditionCreateView, ConditionListView, ConditionUpdateView, ConditionDetailView
from .views import EncounterCreateView, EncounterListView, EncounterUpdateView, EncounterDetailView
from .views import CodeableConceptCreateView, CodeableConceptListView, CodeableConceptUpdateView, CodeableConceptDetailView
from .views import PractitionerCreateView, PractitionerListView, PractitionerUpdateView, PractitionerDetailView
from .views import HealthcareServiceCreateView, HealthcareServiceListView, HealthcareServiceUpdateView, HealthcareServiceDetailView
from .views import DiagnosticReportCreateView, DiagnosticReportListView, DiagnosticReportUpdateView, DiagnosticReportDetailView
# from .views import StatusDokterListView
from .views import daftarTabelListView
# from .views import PatientSearchListView
# from .views import search
urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),

    url(r'^codeableconcept/$', CodeableConceptListView.as_view(), name='codeableconcept_list'),
    url(r'^codeableconcept/new/$', CodeableConceptCreateView.as_view(), name='codeableconcept_add'),
    url(r'^codeableconcept/(?P<pk>\d+)/update/$', CodeableConceptUpdateView.as_view(), name='codeableconcept_update'),
    # url(r'^codeableconcept/(?P<pk>\d+)/detail/$', PatientDetailView.as_view(), name='codeableconcept_detail'),

    url(r'^condition/$', ConditionListView.as_view(), name='condition_list'),
    url(r'^condition/new/$', ConditionCreateView.as_view(), name='condition_add'),
    url(r'^condition/(?P<pk>\d+)/update/$', ConditionUpdateView.as_view(), name='condition_update'),
    url(r'^condition/(?P<pk>\d+)/detail/$', ConditionDetailView.as_view(), name='condition_detail'),

    url(r'^diagnosticreport/$', DiagnosticReportListView.as_view(), name='diagnosticreport_list'),
    url(r'^diagnosticreport/new/$', DiagnosticReportCreateView.as_view(), name='diagnosticReport_add'),
    url(r'^diagnosticreport/(?P<pk>\d+)/update/$', DiagnosticReportUpdateView.as_view(), name='diagnosticreport_update'),
    # url(r'^patient/(?P<pk>\d+)/detail/$', PatientDetailView.as_view(), name='patient_detail'),

    url(r'^encounter/$', EncounterListView.as_view(), name='encounter_list'),
    url(r'^encounter/new/$', EncounterCreateView.as_view(), name='encounter_add'),
    url(r'^encounter/(?P<pk>\d+)/update/$', EncounterUpdateView.as_view(), name='encounter_update'),
    # url(r'^patient/(?P<pk>\d+)/detail/$', PatientDetailView.as_view(), name='patient_detail'),

    url(r'^healthcareservice/$', HealthcareServiceListView.as_view(), name='healthcareservice_list'),
    url(r'^healthcareservice/new/$', HealthcareServiceCreateView.as_view(), name='healthcareService_add'),
    url(r'^healthcareservice/(?P<pk>\d+)/update/$', HealthcareServiceUpdateView.as_view(), name='healthcareservice_update'),
    # url(r'^patient/(?P<pk>\d+)/detail/$', PatientDetailView.as_view(), name='patient_detail'),

    url(r'^location/$', LocationListView.as_view(), name='location_list'),
    url(r'^location/new/$', LocationCreateView.as_view(), name='location_add'),
    url(r'^location/(?P<pk>\d+)/update/$', LocationUpdateView.as_view(), name='location_update'),
    # url(r'^patient/(?P<pk>\d+)/detail/$', PatientDetailView.as_view(), name='patient_detail'),

    url(r'^patient/$', PatientListView.as_view(), name='patient_list'),
    url(r'^patient/new/$', PatientCreateView.as_view(), name='patient_add'),
    url(r'^patient/(?P<pk>\d+)/update/$', PatientUpdateView.as_view(), name='patient_update'),   
    url(r'^patient/(?P<pk>\d+)/detail/$', PatientDetailView.as_view(), name='patient_detail'),   
     
    url(r'^practitioner/$', PractitionerListView.as_view(), name='practitioner_list'),
    url(r'^practitioner/new/$', PractitionerCreateView.as_view(), name='practitioner_add'),
    url(r'^practitioner/(?P<pk>\d+)/update/$', PractitionerUpdateView.as_view(), name='practitioner_update'),
    # url(r'^patient/(?P<pk>\d+)/detail/$', PatientDetailView.as_view(), name='patient_detail'),
    
    url(r'^dashboard/$', views.ubah_status_dokter, name='dashboard'), 
    url(r'^pengaturan/$', views.ubah_status_dokter, name='pengaturan'),   
    url(r'^daftartabel/$', daftarTabelListView.as_view(), name='daftar_tabel'),
    # url(r'^dashboard/$', 'formdemografi.views.search', name='doctor_homepage'),    

    url(r'^pendaftaran/$', daftarTabelListView.as_view(), name='pendaftaran'), 


    # url(r'^teskon/$', views.internet_on, name='kon'),

]
