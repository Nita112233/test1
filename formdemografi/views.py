
# from django.contrib.postgres.search import SearchVector
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from formdemografi import tasks

# from django.contrib.flatpages.models import FlatPage
# from django.template import loader, Context

from django.utils import timezone
from django.db.models import Q
import operator
# from django.views.generic import TemplateView

from django.db import transaction
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from .models import Post
from .forms import PostForm

from .models import ServiceType, statusDokterTersedia
from .models import Reference, CodeableConcept, Coding
from .models import Patient, Practitioner, HealthcareService
from .models import Condition, Evidence, Encounter, DiagnosticReport
from .models import Identifier, Address, Quantity, HumanName, ContactPoint
from .models import Location, Attachment, Period, PractitionerRole

from .forms import AddressForm, AttachmentForm
from .forms import CodeableConceptForm, CodeableConcept_Coding_FormSet
from .forms import CodingForm, ContactPointForm
from .forms import ConditionForm, Condition_Evidence_FormSet, Condition_Identifier_FormSet
from .forms import DiagnosticReportForm, DiagnosticReport_CodeableConcept_FormSet, DiagnosticReport_Attachment_FormSet
from .forms import EvidenceForm, EncounterForm
from .forms import HealthcareServiceForm, HealthcareService_Identifier_FormSet, HealthcareService_ServiceType_FormSet
from .forms import HumanNameForm, IdentifierForm, LocationForm, PeriodForm
from .forms import PatientForm, Patient_Identifier_FormSet, Patient_HumanName_FormSet, Patient_ContactPoint_FormSet, Patient_Address_FormSet, Patient_Attachment_FormSet
from .forms import PractitionerForm, Practitioner_Identifier_FormSet, Practitioner_HumanName_FormSet, Practitioner_PractitionerRole_FormSet
from .forms import PractitionerRoleForm, QuantityForm, statusDokterTersediaForm

import urllib2

# def foo(request):
#     r = tasks.add.delay(2, 2)
#     return HttpResponse(r.task_id)

# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'formdemografi/post_list.html', {'posts': posts})

# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'formdemografi/post_detail.html', {'post': post})

# def post_new(request):
#     form = PostForm()
#     return render(request, 'formdemografi/post_edit.html', {'form': form})

# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False) 
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'formdemografi/post_edit.html', {'form': form})

# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'formdemografi/post_edit.html', {'form': form})

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++

def ubah_status_dokter(request):
    form = statusDokterTersediaForm()
    return render(request, 'formdemografi/pengaturan.html', {'form': form})

def ubah_status_dokter(request):
    if request.method == "POST":
        form = statusDokterTersediaForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False) 
            status.id_user = request.user
            status.date_created = timezone.now()
            status.save()
            return redirect('/dashboard', pk=statusDokterTersedia.pk)
    else:
        form = statusDokterTersediaForm()
    return render(request, 'formdemografi/pengaturan.html', {'form': form})
    
class daftarTabelListView(ListView):
    model = statusDokterTersedia
    form_class = statusDokterTersediaForm
    template_name = 'formdemografi/daftar_tabel.html'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class PatientListView(ListView):
    model = Patient
    form_class = PatientForm

class PatientDetailView(DetailView):
    model = Patient

class PatientCreateView(CreateView):
    template_name = 'formdemografi/patient_add.html'
    model = Patient
    form_class = PatientForm
    success_url=reverse_lazy('formdemografi:patient_list')

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        patient_identifier_formset = Patient_Identifier_FormSet()
        patient_humanname_formset = Patient_HumanName_FormSet()
        patient_contactpoint_formset = Patient_ContactPoint_FormSet()
        patient_address_formset = Patient_Address_FormSet()
        patient_attachment_formset = Patient_Attachment_FormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  patient_identifier_formset=patient_identifier_formset,
                                  patient_humanname_formset=patient_humanname_formset,
                                  patient_contactpoint_formset=patient_contactpoint_formset,
                                  patient_address_formset=patient_address_formset,
                                  patient_attachment_formset=patient_attachment_formset,
                                  ))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        patient_identifier_formset = Patient_Identifier_FormSet(self.request.POST)
        patient_humanname_formset = Patient_HumanName_FormSet(self.request.POST)
        patient_contactpoint_formset = Patient_ContactPoint_FormSet(self.request.POST)
        patient_address_formset = Patient_Address_FormSet(self.request.POST)
        patient_attachment_formset = Patient_Attachment_FormSet(self.request.POST)
        if (form.is_valid() and 
            patient_identifier_formset.is_valid() and
            patient_humanname_formset.is_valid() and
            patient_contactpoint_formset.is_valid() and
            patient_address_formset.is_valid() and
            patient_attachment_formset.is_valid()
            ):
            return self.form_valid(form, patient_identifier_formset, patient_humanname_formset, patient_contactpoint_formset, patient_address_formset, patient_attachment_formset)
        else:
            return self.form_invalid(form, patient_identifier_formset, patient_humanname_formset, patient_contactpoint_formset, patient_address_formset, patient_attachment_formset)

    def form_valid(self, form, patient_identifier_formset, patient_humanname_formset, patient_contactpoint_formset, patient_address_formset, patient_attachment_formset):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        patient_identifier_formset.instance = self.object
        patient_identifier_formset.save()
        patient_humanname_formset.instance = self.object
        patient_humanname_formset.save()
        patient_contactpoint_formset.instance = self.object
        patient_contactpoint_formset.save()
        patient_address_formset.instance = self.object
        patient_address_formset.save()
        patient_attachment_formset.instance = self.object
        patient_attachment_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, patient_identifier_formset, patient_humanname_formset, patient_contactpoint_formset, patient_address_formset, patient_attachment_formset):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  patient_identifier_formset=patient_identifier_formset,
                                  patient_humanname_formset=patient_humanname_formset,
                                  patient_contactpoint_formset=patient_contactpoint_formset,
                                  patient_address_formset=patient_address_formset,
                                  patient_attachment_formset=patient_attachment_formset,
                                  ))

class PatientUpdateView(UpdateView):
    template_name = 'formdemografi/patient_add.html'
    model = Patient
    form_class = PatientForm
    success_url=reverse_lazy('formdemografi:patient_list')

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        patient_identifier_formset = Patient_Identifier_FormSet(instance = self.object)
        patient_humanname_formset = Patient_HumanName_FormSet(instance = self.object)
        patient_contactpoint_formset = Patient_ContactPoint_FormSet(instance = self.object)
        patient_address_formset = Patient_Address_FormSet(instance = self.object)
        patient_attachment_formset = Patient_Attachment_FormSet(instance = self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  patient_identifier_formset=patient_identifier_formset,
                                  patient_humanname_formset=patient_humanname_formset,
                                  patient_contactpoint_formset=patient_contactpoint_formset,
                                  patient_address_formset=patient_address_formset,
                                  patient_attachment_formset=patient_attachment_formset,
                                  ))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        patient_identifier_formset = Patient_Identifier_FormSet(self.request.POST, instance=self.object)
        patient_humanname_formset = Patient_HumanName_FormSet(self.request.POST, instance=self.object)
        patient_contactpoint_formset = Patient_ContactPoint_FormSet(self.request.POST, instance=self.object)
        patient_address_formset = Patient_Address_FormSet(self.request.POST, instance=self.object)
        patient_attachment_formset = Patient_Attachment_FormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and 
            patient_identifier_formset.is_valid() and
            patient_humanname_formset.is_valid() and
            patient_contactpoint_formset.is_valid() and
            patient_address_formset.is_valid() and
            patient_attachment_formset.is_valid()
            ):
            return self.form_valid(form, patient_identifier_formset, patient_humanname_formset, patient_contactpoint_formset, patient_address_formset, patient_attachment_formset)
        else:
            return self.form_invalid(form, patient_identifier_formset, patient_humanname_formset, patient_contactpoint_formset, patient_address_formset, patient_attachment_formset)

    def form_valid(self, form, patient_identifier_formset, patient_humanname_formset, patient_contactpoint_formset, patient_address_formset, patient_attachment_formset):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        patient_identifier_formset.instance = self.object
        patient_identifier_formset.save()
        patient_humanname_formset.instance = self.object
        patient_humanname_formset.save()
        patient_contactpoint_formset.instance = self.object
        patient_contactpoint_formset.save()
        patient_address_formset.instance = self.object
        patient_address_formset.save()
        patient_attachment_formset.instance = self.object
        patient_attachment_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, patient_identifier_formset, patient_humanname_formset, patient_contactpoint_formset, patient_address_formset, patient_attachment_formset):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  patient_identifier_formset=patient_identifier_formset,
                                  patient_humanname_formset=patient_humanname_formset,
                                  patient_contactpoint_formset=patient_contactpoint_formset,
                                  patient_address_formset=patient_address_formset,
                                  patient_attachment_formset=patient_attachment_formset,
                                  ))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# [CONDITION] done

class ConditionListView(ListView):
    model = Condition
    form_class = ConditionForm

class ConditionDetailView(DetailView):
    model = Condition

class ConditionCreateView(CreateView):
    template_name = 'formdemografi/condition_add.html'
    model = Condition
    form_class = ConditionForm
    success_url=reverse_lazy('formdemografi:condition_list')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        condition_identifier_formset = Condition_Identifier_FormSet()
        condition_evidence_formset = Condition_Evidence_FormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  condition_identifier_formset=condition_identifier_formset,
                                  condition_evidence_formset=condition_evidence_formset,
                                  ))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        condition_identifier_formset = Condition_Identifier_FormSet(self.request.POST)
        condition_evidence_formset = Condition_Evidence_FormSet(self.request.POST)
        if (form.is_valid() and 
            condition_identifier_formset.is_valid() and
            condition_evidence_formset.is_valid()
            ):
            return self.form_valid(form, condition_identifier_formset, condition_evidence_formset)
        else:
            return self.form_invalid(form, condition_identifier_formset, condition_evidence_formset)

    def form_valid(self, form, condition_identifier_formset, condition_evidence_formset):
        self.object = form.save()
        condition_identifier_formset.instance = self.object
        condition_identifier_formset.save()
        condition_evidence_formset.instance = self.object
        condition_evidence_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, condition_identifier_formset, condition_evidence_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  condition_identifier_formset=condition_identifier_formset,
                                  condition_evidence_formset=condition_evidence_formset,
                                  ))

class ConditionUpdateView(UpdateView):
    template_name = 'formdemografi/condition_add.html'
    model = Condition
    form_class = ConditionForm
    success_url=reverse_lazy('formdemografi:condition_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        condition_identifier_formset = Condition_Identifier_FormSet(instance = self.object)
        condition_evidence_formset = Condition_Evidence_FormSet(instance = self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  condition_identifier_formset=condition_identifier_formset,
                                  condition_evidence_formset=condition_evidence_formset,
                                  ))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        condition_identifier_formset = Condition_Identifier_FormSet(self.request.POST, instance=self.object)
        condition_evidence_formset = Condition_Evidence_FormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and 
            condition_identifier_formset.is_valid() and
            condition_evidence_formset.is_valid()
            ):
            return self.form_valid(form, condition_identifier_formset, condition_evidence_formset)
        else:
            return self.form_invalid(form, condition_identifier_formset, condition_evidence_formset)

    def form_valid(self, form, condition_identifier_formset, condition_evidence_formset):
        self.object = form.save()
        condition_identifier_formset.instance = self.object
        condition_identifier_formset.save()
        condition_evidence_formset.instance = self.object
        condition_evidence_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, condition_identifier_formset, condition_evidence_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  condition_identifier_formset=condition_identifier_formset,
                                  condition_evidence_formset=condition_evidence_formset,
                                  ))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# [ENCOUNTER] not DONE

class EncounterListView(ListView):
    model = Encounter
    form_class = EncounterForm

class EncounterDetailView(DetailView):
    model = Encounter

class EncounterCreateView(CreateView):
    template_name = 'formdemografi/encounter_add.html'
    model = Encounter
    form_class = EncounterForm
    success_url=reverse_lazy('formdemografi:encounter_list')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        patient_identifier_formset = Patient_Identifier_FormSet()
        patient_humanname_formset = Patient_HumanName_FormSet()
        patient_contactpoint_formset = Patient_ContactPoint_FormSet()
        patient_address_formset = Patient_Address_FormSet()
        patient_attachment_formset = Patient_Attachment_FormSet()
        patient_contact_formset = Patient_Contact_FormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  patient_identifier_formset=patient_identifier_formset,
                                  patient_humanname_formset=patient_humanname_formset,
                                  patient_contactpoint_formset=patient_contactpoint_formset,
                                  patient_address_formset=patient_address_formset,
                                  patient_attachment_formset=patient_attachment_formset,
                                  patient_contact_formset=patient_contact_formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        patient_identifier_formset = Patient_Identifier_FormSet(self.request.POST)
        patient_humanname_formset = Patient_HumanName_FormSet(self.request.POST)
        if (form.is_valid() and 
            patient_identifier_formset.is_valid() and
            patient_humanname_formset.is_valid() and
            patient_contactpoint_formset.is_valid() and
            patient_address_formset.is_valid() and
            patient_attachment_formset.is_valid() and
            patient_contact_formset.is_valid()
            ):
            return self.form_valid(form, patient_identifier_formset, patient_humanname_formset)
        else:
            return self.form_invalid(form, patient_identifier_formset, patient_humanname_formset)

    def form_valid(self, form, ingredient_form, instruction_form):
        self.object = form.save()
        patient_identifier_formset.instance = self.object
        patient_identifier_formset.save()
        patient_humanname_formset.instance = self.object
        patient_humanname_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ingredient_form, instruction_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  patient_identifier_formset=patient_identifier_formset,
                                  patient_humanname_formset=patient_humanname_formset))

class EncounterUpdateView(UpdateView):
    template_name = 'formdemografi/encounter_add.html'
    model = Encounter
    form_class = EncounterForm
    success_url=reverse_lazy('formdemografi:encounter_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        patient_identifier_formset = Patient_Identifier_FormSet(instance = self.object)
        patient_humanname_formset = Patient_HumanName_FormSet(instance = self.object)
        patient_contactpoint_formset = Patient_ContactPoint_FormSet(instance = self.object)
        patient_address_formset = Patient_Address_FormSet(instance = self.object)
        patient_attachment_formset = Patient_Attachment_FormSet(instance = self.object)
        patient_contact_formset = Patient_Contact_FormSet(instance = self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  patient_identifier_formset=patient_identifier_formset,
                                  patient_humanname_formset=patient_humanname_formset,
                                  patient_contactpoint_formset=patient_contactpoint_formset,
                                  patient_address_formset=patient_address_formset,
                                  patient_attachment_formset=patient_attachment_formset,
                                  patient_contact_formset=patient_contact_formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        patient_identifier_formset = Patient_Identifier_FormSet(self.request.POST, instance=self.object)
        patient_humanname_formset = Patient_HumanName_FormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and 
            patient_identifier_formset.is_valid() and
            patient_humanname_formset.is_valid() and
            patient_contactpoint_formset.is_valid() and
            patient_address_formset.is_valid() and
            patient_attachment_formset.is_valid() and
            patient_contact_formset.is_valid()
            ):
            return self.form_valid(form, patient_identifier_formset, patient_humanname_formset)
        else:
            return self.form_invalid(form, patient_identifier_formset, patient_humanname_formset)

    def form_valid(self, form, ingredient_form, instruction_form):
        self.object = form.save()
        patient_identifier_formset.instance = self.object
        patient_identifier_formset.save()
        patient_humanname_formset.instance = self.object
        patient_humanname_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ingredient_form, instruction_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  patient_identifier_formset=patient_identifier_formset,
                                  patient_humanname_formset=patient_humanname_formset))


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# [CODEABLECONCEPT] done

class CodeableConceptListView(ListView):
    model = CodeableConcept
    form_class = CodeableConceptForm

class CodeableConceptDetailView(DetailView):
    model = CodeableConcept

class CodeableConceptCreateView(CreateView):
    template_name = 'formdemografi/codeableconcept_add.html'
    model = CodeableConcept
    form_class = CodeableConceptForm
    success_url=reverse_lazy('formdemografi:codeableconcept_list')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        codeableconcept_coding_formset = CodeableConcept_Coding_FormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  codeableconcept_coding_formset=codeableconcept_coding_formset,
                                  ))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        codeableconcept_coding_formset = CodeableConcept_Coding_FormSet(self.request.POST)
        if (form.is_valid() and 
            codeableconcept_coding_formset.is_valid()
            ):
            return self.form_valid(form, codeableconcept_coding_formset)
        else:
            return self.form_invalid(form, codeableconcept_coding_formset)

    def form_valid(self, form, icodeableconcept_coding_formset):
        self.object = form.save()
        codeableconcept_coding_formset.instance = self.object
        codeableconcept_coding_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, icodeableconcept_coding_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  codeableconcept_coding_formset=codeableconcept_coding_formset))

class CodeableConceptUpdateView(UpdateView):
    template_name = 'formdemografi/codeableconcept_add.html'
    model = CodeableConcept
    form_class = CodeableConceptForm
    success_url=reverse_lazy('formdemografi:codeableconcept_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        codeableconcept_coding_formset = CodeableConcept_Coding_FormSet(instance = self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  codeableconcept_coding_formset=codeableconcept_coding_formset,
                                  ))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        codeableconcept_coding_formset = CodeableConcept_Coding_FormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and 
            codeableconcept_coding_formset.is_valid()
            ):
            return self.form_valid(form, codeableconcept_coding_formset)
        else:
            return self.form_invalid(form, codeableconcept_coding_formset)

    def form_valid(self, form, icodeableconcept_coding_formset):
        self.object = form.save()
        codeableconcept_coding_formset.instance = self.object
        codeableconcept_coding_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, icodeableconcept_coding_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  codeableconcept_coding_formset=codeableconcept_coding_formset))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# [Practitioner] done

class PractitionerListView(ListView):
    model = Practitioner
    form_class = PractitionerForm

class PractitionerDetailView(DetailView):
    model = Practitioner

class PractitionerCreateView(CreateView):
    template_name = 'formdemografi/practitioner_add.html'
    model = Practitioner
    form_class = PractitionerForm
    success_url=reverse_lazy('formdemografi:practitioner_list')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        practitioner_identifier_formset = Practitioner_Identifier_FormSet()
        practitioner_humanname_formset = Practitioner_HumanName_FormSet()
        practitioner_practitionerrole_formset = Practitioner_PractitionerRole_FormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  practitioner_identifier_formset=practitioner_identifier_formset,
                                  practitioner_humanname_formset=practitioner_humanname_formset,
                                  practitioner_practitionerrole_formset=practitioner_practitionerrole_formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        practitioner_identifier_formset = Practitioner_Identifier_FormSet(self.request.POST)
        practitioner_humanname_formset = Practitioner_HumanName_FormSet(self.request.POST)
        practitioner_practitionerrole_formset = Practitioner_PractitionerRole_FormSet(self.request.POST)
        if (form.is_valid() and 
            practitioner_identifier_formset.is_valid() and
            practitioner_humanname_formset.is_valid() and
            practitioner_practitionerrole_formset.is_valid()
            ):
            return self.form_valid(form, practitioner_identifier_formset, practitioner_humanname_formset, practitioner_practitionerrole_formset)
        else:
            return self.form_invalid(form, practitioner_identifier_formset, practitioner_humanname_formset, practitioner_practitionerrole_formset)

    def form_valid(self, form, practitioner_identifier_formset, practitioner_humanname_formset, practitioner_practitionerrole_formset):
        self.object = form.save()
        practitioner_identifier_formset.instance = self.object
        practitioner_identifier_formset.save()
        practitioner_humanname_formset.instance = self.object
        practitioner_humanname_formset.save()
        practitioner_practitionerrole_formset.instance = self.object
        practitioner_practitionerrole_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, practitioner_identifier_formset, practitioner_humanname_formset, practitioner_practitionerrole_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  practitioner_identifier_formset=practitioner_identifier_formset,
                                  practitioner_humanname_formset=practitioner_humanname_formset,
                                  practitioner_practitionerrole_formset=practitioner_practitionerrole_formset))

class PractitionerUpdateView(UpdateView):
    template_name = 'formdemografi/practitioner_add.html'
    model = Practitioner
    form_class = PractitionerForm
    success_url=reverse_lazy('formdemografi:practitioner_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        practitioner_identifier_formset = Practitioner_Identifier_FormSet(instance = self.object)
        practitioner_humanname_formset = Practitioner_HumanName_FormSet(instance = self.object)
        practitioner_practitionerrole_formset = Practitioner_PractitionerRole_FormSet(instance = self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  practitioner_identifier_formset=practitioner_identifier_formset,
                                  practitioner_humanname_formset=practitioner_humanname_formset,
                                  practitioner_practitionerrole_formset=practitioner_practitionerrole_formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        practitioner_identifier_formset = Practitioner_Identifier_FormSet(self.request.POST, instance=self.object)
        practitioner_humanname_formset = Practitioner_HumanName_FormSet(self.request.POST, instance=self.object)
        practitioner_practitionerrole_formset = Practitioner_PractitionerRole_FormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and 
            practitioner_identifier_formset.is_valid() and
            practitioner_humanname_formset.is_valid() and
            practitioner_practitionerrole_formset.is_valid()
            ):
            return self.form_valid(form, practitioner_identifier_formset, practitioner_humanname_formset, practitioner_practitionerrole_formset)
        else:
            return self.form_invalid(form, practitioner_identifier_formset, practitioner_humanname_formset, practitioner_practitionerrole_formset)

    def form_valid(self, form, practitioner_identifier_formset, practitioner_humanname_formset, practitioner_practitionerrole_formset):
        self.object = form.save()
        practitioner_identifier_formset.instance = self.object
        practitioner_identifier_formset.save()
        practitioner_humanname_formset.instance = self.object
        practitioner_humanname_formset.save()
        practitioner_practitionerrole_formset.instance = self.object
        practitioner_practitionerrole_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, practitioner_identifier_formset, practitioner_humanname_formset, practitioner_practitionerrole_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  practitioner_identifier_formset=practitioner_identifier_formset,
                                  practitioner_humanname_formset=practitioner_humanname_formset,
                                  practitioner_practitionerrole_formset=practitioner_practitionerrole_formset))


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# [HealthcareService] done

class HealthcareServiceListView(ListView):
    model = HealthcareService
    form_class = HealthcareServiceForm

class HealthcareServiceDetailView(DetailView):
    model = HealthcareService

class HealthcareServiceCreateView(CreateView):
    template_name = 'formdemografi/healthcareservice_add.html'
    model = HealthcareService
    form_class = HealthcareServiceForm
    success_url=reverse_lazy('formdemografi:healthcareservice_list')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        healthcareservice_identifier_formset = HealthcareService_Identifier_FormSet()
        healthcareservice_servicetype_formset = HealthcareService_ServiceType_FormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  healthcareservice_identifier_formset=healthcareservice_identifier_formset,
                                  healthcareservice_servicetype_formset=healthcareservice_servicetype_formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        healthcareservice_identifier_formset = HealthcareService_Identifier_FormSet(self.request.POST)
        healthcareservice_servicetype_formset = HealthcareService_ServiceType_FormSet(self.request.POST)
        if (form.is_valid() and 
            healthcareservice_identifier_formset.is_valid() and
            healthcareservice_servicetype_formset.is_valid()
            ):
            return self.form_valid(form, healthcareservice_identifier_formset, healthcareservice_servicetype_formset)
        else:
            return self.form_invalid(form, healthcareservice_identifier_formset, healthcareservice_servicetype_formset)

    def form_valid(self, form, healthcareservice_identifier_formset, healthcareservice_servicetype_formset):
        self.object = form.save()
        healthcareservice_identifier_formset.instance = self.object
        healthcareservice_identifier_formset.save()
        healthcareservice_servicetype_formset.instance = self.object
        healthcareservice_servicetype_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, healthcareservice_identifier_formset, healthcareservice_servicetype_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  healthcareservice_identifier_formset=healthcareservice_identifier_formset,
                                  healthcareservice_servicetype_formset=healthcareservice_servicetype_formset))

class HealthcareServiceUpdateView(UpdateView):
    template_name = 'formdemografi/healthcareservice_add.html'
    model = HealthcareService
    form_class = HealthcareServiceForm
    success_url=reverse_lazy('formdemografi:healthcareservice_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        healthcareservice_identifier_formset = HealthcareService_Identifier_FormSet(instance = self.object)
        healthcareservice_servicetype_formset = HealthcareService_ServiceType_FormSet(instance = self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  healthcareservice_identifier_formset=healthcareservice_identifier_formset,
                                  healthcareservice_servicetype_formset=healthcareservice_servicetype_formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        healthcareservice_identifier_formset = HealthcareService_Identifier_FormSet(self.request.POST, instance=self.object)
        healthcareservice_servicetype_formset = HealthcareService_ServiceType_FormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and 
            healthcareservice_identifier_formset.is_valid() and
            healthcareservice_servicetype_formset.is_valid()
            ):
            return self.form_valid(form, healthcareservice_identifier_formset, healthcareservice_servicetype_formset)
        else:
            return self.form_invalid(form, healthcareservice_identifier_formset, healthcareservice_servicetype_formset)

    def form_valid(self, form, healthcareservice_identifier_formset, healthcareservice_servicetype_formset):
        self.object = form.save()
        healthcareservice_identifier_formset.instance = self.object
        healthcareservice_identifier_formset.save()
        healthcareservice_servicetype_formset.instance = self.object
        healthcareservice_servicetype_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, healthcareservice_identifier_formset, healthcareservice_servicetype_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  healthcareservice_identifier_formset=healthcareservice_identifier_formset,
                                  healthcareservice_servicetype_formset=healthcareservice_servicetype_formset))


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# [Location] done
class LocationListView(ListView):
    model = Location
    form_class = LocationForm

class LocationDetailView(DetailView):
    model = Location

class LocationCreateView(CreateView):
    template_name = 'formdemografi/location_add.html'
    model = Location
    form_class = LocationForm
    success_url=reverse_lazy('formdemografi:location_list')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(
            self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if (form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


    # def get(self, request, *args, **kwargs):
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     location_identifier_formset = Location_Identifier_FormSet()
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               location_identifier_formset=location_identifier_formset))

    # def post(self, request, *args, **kwargs):
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     location_identifier_formset = Location_Identifier_FormSet(self.request.POST)
    #     if (form.is_valid() and 
    #         location_identifier_formset.is_valid()
    #         ):
    #         return self.form_valid(form, location_identifier_formset)
    #     else:
    #         return self.form_invalid(form, location_identifier_formset)

    # def form_valid(self, form, location_identifier_formset):
    #     self.object = form.save()
    #     location_identifier_formset.instance = self.object
    #     location_identifier_formset.save()
    #     return HttpResponseRedirect(self.get_success_url())

    # def form_invalid(self, form, location_identifier_formset):
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               location_identifier_formset=location_identifier_formset))

class LocationUpdateView(UpdateView):
    template_name = 'formdemografi/location_add.html'
    model = Location
    form_class = LocationForm
    success_url=reverse_lazy('formdemografi:location_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(
            self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if (form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class DiagnosticReportListView(ListView):
    model = DiagnosticReport
    form_class = DiagnosticReportForm

class DiagnosticReportDetailView(DetailView):
    model = DiagnosticReport

class DiagnosticReportCreateView(CreateView):
    template_name = 'formdemografi/diagnosticreport_add.html'
    model = DiagnosticReport
    form_class = DiagnosticReportForm
    success_url=reverse_lazy('formdemografi:diagnosticreport_list')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        diagnosticreport_codeableconcept_formset = DiagnosticReport_CodeableConcept_FormSet()
        diagnosticreport_attachment_formset = DiagnosticReport_Attachment_FormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  diagnosticreport_codeableconcept_formset=diagnosticreport_codeableconcept_formset,
                                  diagnosticreport_attachment_formset=diagnosticreport_attachment_formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        diagnosticreport_codeableconcept_formset = DiagnosticReport_CodeableConcept_FormSet(self.request.POST)
        diagnosticreport_attachment_formset = DiagnosticReport_Attachment_FormSet(self.request.POST)
        if (form.is_valid() and 
            diagnosticreport_codeableconcept_formset.is_valid() and
            diagnosticreport_attachment_formset.is_valid()
            ):
            return self.form_valid(form, diagnosticreport_codeableconcept_formset, diagnosticreport_attachment_formset)
        else:
            return self.form_invalid(form, diagnosticreport_codeableconcept_formset, diagnosticreport_attachment_formset)

    def form_valid(self, form, diagnosticreport_codeableconcept_formset, diagnosticreport_attachment_formset):
        self.object = form.save()
        diagnosticreport_codeableconcept_formset.instance = self.object
        diagnosticreport_codeableconcept_formset.save()
        diagnosticreport_attachment_formset.instance = self.object
        diagnosticreport_attachment_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, diagnosticreport_codeableconcept_formset, diagnosticreport_attachment_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  diagnosticreport_codeableconcept_formset=diagnosticreport_codeableconcept_formset,
                                  diagnosticreport_attachment_formset=diagnosticreport_attachment_formset))

class DiagnosticReportUpdateView(UpdateView):
    template_name = 'formdemografi/diagnosticreport_add.html'
    model = DiagnosticReport
    form_class = DiagnosticReportForm
    success_url=reverse_lazy('formdemografi:diagnosticreport_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        diagnosticreport_codeableconcept_formset = DiagnosticReport_CodeableConcept_FormSet(instance = self.object)
        diagnosticreport_attachment_formset = DiagnosticReport_Attachment_FormSet(instance = self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  diagnosticreport_codeableconcept_formset=diagnosticreport_codeableconcept_formset,
                                  diagnosticreport_attachment_formset=diagnosticreport_attachment_formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        diagnosticreport_codeableconcept_formset = DiagnosticReport_CodeableConcept_FormSet(self.request.POST, instance=self.object)
        diagnosticreport_attachment_formset = DiagnosticReport_Attachment_FormSet(self.request.POST, instance=self.object)
        if (form.is_valid() and 
            diagnosticreport_codeableconcept_formset.is_valid() and
            diagnosticreport_attachment_formset.is_valid()
            ):
            return self.form_valid(form, diagnosticreport_codeableconcept_formset, diagnosticreport_attachment_formset)
        else:
            return self.form_invalid(form, diagnosticreport_codeableconcept_formset, diagnosticreport_attachment_formset)

    def form_valid(self, form, diagnosticreport_codeableconcept_formset, diagnosticreport_attachment_formset):
        self.object = form.save()
        diagnosticreport_codeableconcept_formset.instance = self.object
        diagnosticreport_codeableconcept_formset.save()
        diagnosticreport_attachment_formset.instance = self.object
        diagnosticreport_attachment_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, diagnosticreport_codeableconcept_formset, diagnosticreport_attachment_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  diagnosticreport_codeableconcept_formset=diagnosticreport_codeableconcept_formset,
                                  diagnosticreport_attachment_formset=diagnosticreport_attachment_formset))

