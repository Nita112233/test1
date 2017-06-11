from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Post

# from .models import TimeStampedModel, AddMedicalRecord
from .models import ServiceType, statusDokterTersedia
from .models import Reference, CodeableConcept, Coding
from .models import Patient, Practitioner, HealthcareService
from .models import Condition, Evidence, Encounter, DiagnosticReport
from .models import Identifier, Address, Quantity, HumanName, ContactPoint
from .models import Location, Attachment, Period, PractitionerRole

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')

class statusDokterTersediaForm(forms.ModelForm):
    class Meta:
        model = statusDokterTersedia
        fields = ('SedangPraktek',)

class CodingForm(forms.ModelForm):
    class Meta:
        model = Coding
        fields = ('system', 'version', 'code', 'display', 'userSelected')
# diisi dr awal, ga diisi ma dokter, tp bs diisi oleh admin
class CodeableConceptForm(forms.ModelForm):
    class Meta:
        model = CodeableConcept
        fields = ('text',)
CodeableConcept_Coding_FormSet = inlineformset_factory(CodeableConcept, Coding, form=CodingForm, extra=1, max_num=1000)

class IdentifierForm(forms.ModelForm):
    class Meta:
        model = Identifier
        fields = ('Type', 'Value',)

class HumanNameForm(forms.ModelForm):
    class Meta:
        model = HumanName
        fields = ('text', 'family', 'given')

class ContactPointForm(forms.ModelForm):
    class Meta:
        model = ContactPoint
        fields = ('system', 'Value',)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('Type', 'text', 'line', 'city', 'district', 'state', 'postalCode', 'country',)

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('url', 'title',)
# pending

class EvidenceForm(forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ('code', 'detail')

class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = ('code', 'category', 'bodySite', 'notes')
# identifier, reference
Condition_Identifier_FormSet = inlineformset_factory(Condition, Identifier, form=IdentifierForm, extra=1, max_num=1000)
Condition_Evidence_FormSet = inlineformset_factory(Condition, Evidence, form=EvidenceForm, extra=1, max_num=1000)
# Condition_Reference_FormSet = inlineformset_factory(Condition, Reference, form=ReferenceForm, extra=1, max_num=1)


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('active', 'gender', 'birthDate', 'deceasedBoolean', 'deceasedDateTime', 'maritalStatus','language')
Patient_Identifier_FormSet = inlineformset_factory(Patient, Identifier, form=IdentifierForm, extra=3, max_num=1000)
Patient_HumanName_FormSet = inlineformset_factory(Patient, HumanName, form=HumanNameForm, extra=1, max_num=1000)
Patient_ContactPoint_FormSet = inlineformset_factory(Patient, ContactPoint, form=ContactPointForm, extra=2, max_num=1000)
Patient_Address_FormSet = inlineformset_factory(Patient, Address, form=AddressForm, extra=1, max_num=1000)
Patient_Attachment_FormSet = inlineformset_factory(Patient, Attachment, form=AttachmentForm, extra=1, max_num=1000)
Patient_Condition_FormSet = inlineformset_factory(Patient, Condition, form=ConditionForm, extra=1, max_num=1000)

class PractitionerRoleForm(forms.ModelForm):
    class Meta:
        model = PractitionerRole
        fields = ('role', 'specialty')

class PractitionerForm(forms.ModelForm):
    class Meta:
        model = Practitioner
        fields = ()
Practitioner_Identifier_FormSet = inlineformset_factory(Practitioner, Identifier, form=IdentifierForm, extra=1, max_num=1000)
Practitioner_HumanName_FormSet = inlineformset_factory(Practitioner, HumanName, form=HumanNameForm, extra=2, max_num=60)
Practitioner_PractitionerRole_FormSet = inlineformset_factory(Practitioner, PractitionerRole, form=PractitionerRoleForm, extra=2, max_num=1000)

class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = ('Type',)

class HealthcareServiceForm(forms.ModelForm):
    class Meta:
        model = HealthcareService
        fields = ('serviceCategory', 'serviceName')
HealthcareService_Identifier_FormSet = inlineformset_factory(HealthcareService, Identifier, form=IdentifierForm, extra=1, max_num=1000)
HealthcareService_ServiceType_FormSet = inlineformset_factory(HealthcareService, ServiceType, form=ServiceTypeForm, extra=1, max_num=1000)
# kurang reference

class QuantityForm(forms.ModelForm):
    class Meta:
        model = Quantity
        fields = ('Value', 'comparator', 'unit')

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'description')
# pending
# Location_Identifier_FormSet = inlineformset_factory(Location, Identifier, form=IdentifierForm, extra=1, max_num=1000)


class EncounterForm(forms.ModelForm):
    class Meta:
        model = Encounter
        fields = ('Class', 'reason')
# identifier, reference, reason
Encounter_identifier_FormSet = inlineformset_factory(Encounter, Identifier, form=IdentifierForm, extra=1, max_num=1000)

class DiagnosticReportForm(forms.ModelForm):
    class Meta:
        model = DiagnosticReport
        fields = ('status', 'category', 'code', 'effectiveDateTime', 'conclusion')
# identifier, reference, status, category, code, reference, 
DiagnosticReport_CodeableConcept_FormSet = inlineformset_factory(DiagnosticReport, CodeableConcept, form=CodeableConceptForm, extra=1, max_num=1000)
DiagnosticReport_Attachment_FormSet = inlineformset_factory(DiagnosticReport, Attachment, form=AttachmentForm, extra=1, max_num=1000)

class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ('start', 'end')

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ('reference', 'display')










