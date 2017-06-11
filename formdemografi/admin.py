from django.contrib import admin

from .models import Post
from .models import Patient, Condition, Evidence, Identifier, Address, HumanName
from .models import ContactPoint, Location, Attachment
# from .models import ServiceType, Reference, CodeableConcept, Coding
# from .models import Practitioner, HealthcareService, Encounter, DiagnosticReport
# from .models import Quantity, Period, PractitionerRole

class IdentifierInline(admin.TabularInline):
    model = Identifier
    extra = 1

class HumanNameInline(admin.TabularInline):
    model = HumanName
    extra = 1

class ContactPointInline(admin.TabularInline):
    model = ContactPoint
    extra = 1

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 1

class PatientAdmin(admin.ModelAdmin):
    inlines = [
        IdentifierInline, HumanNameInline, ContactPointInline, AddressInline,
        AttachmentInline, 
    ]

class ConditionAdmin(admin.ModelAdmin):
    inlines = [
        IdentifierInline, EvidenceInline,
    ]

admin.site.register(Post)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Condition, ConditionAdmin)

# admin.site.register(Post, ServiceType, Reference, CodeableConcept, Coding, Practitioner, 
# HealthcareService, Condition, Evidence, Encounter, DiagnosticReport, Identifier, 
# Address, Quantity, HumanName, ContactPoint, Location, Attachment, Period, 
# PractitionerRole) #register the model
# http://stackoverflow.com/questions/30472741/inlinemodeladmin-not-showing-up-on-admin-page