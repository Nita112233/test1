from __future__ import unicode_literals
# import uuid
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

# example django-queued-storage
# from queued_storage.fields import QueuedFileField
# from queued_storage.backends import QueuedStorage
# queued_s3storage = QueuedStorage(
#     'django.core.files.storage.FileSystemStorage',
#     'storages.backends.s3boto.S3BotoStorage', 
#     task='queued_storage.tasks.TransferAndDelete')

# class MyModel(models.Model):
#     my_file = models.FileField(upload_to='files', storage=queued_s3storage)

###############################

# class petugasrekammedis(models.Model):
#     user = models.OneToOneField(User)
#     SedangPraktek = models.BooleanField( # 
#         default = False)

# class petugaspendaftaran(models.Model):
#    user = models.OneToOneField(User)

# user = User.objects.create_user(username='dokterA',
#                                 password='8semutapikacau')

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# ++++++++++++++++++++++++++++++++++++++++++++

class statusDokterTersedia(models.Model):
    id_user = models.ForeignKey('auth.User')
    KETERSEDIAAN_CHOICES = (
        ("off", 'Sedang tidak praktek'),
        ("on", 'Sedang praktek'),
    )
    SedangPraktek = models.CharField(
        choices = KETERSEDIAAN_CHOICES,
        max_length = 25,
        default=False,
        verbose_name = "Status anda",
        blank = True)
    date_created = models.DateTimeField(
        primary_key = True,
        default=timezone.now)

    def status_dokter(self):
        current_user = request.user
        return self.current_user

class tabel_sinkronisasi_cloud(models.Model):
    id_transaksi_cloud = models.CharField(
        max_length = 20,
        primary_key=True)
    date_received = models.DateTimeField(
        default=timezone.now)
    tbl_client = models.OneToOneField(
        'tabel_sinkronisasi_client',
        # on_delete=models.CASCADE,
        # primary_key=True,
    )

class tabel_sinkronisasi_client(models.Model):
    id_user = models.ForeignKey('auth.User')
    # patient = models.ForeignKey('Patient', null=True, on_delete=models.CASCADE)
    id_transaksi_client = models.CharField(
        primary_key=True,
        max_length = 50,)
    status_sinkronisasi = models.CharField(
        default='0',
        max_length = 1)
    status_edit = models.CharField(
        default='0',
        max_length = 1)
    # no_rekam_medis = models.CharField(
    #     max_length = 50,
    #     unique = True)    
    date_created = models.DateTimeField(
        default=timezone.now)
    # date_uploaded belum edit nyambung sama script
    date_uploaded = models.DateTimeField(
        default=timezone.now)
    
    class Meta:
        unique_together = (("id_user", "id_transaksi_client"),)

    def stat_sinkron(self):
        status_sinkronisasi = request.user
        return self.current_user

class arsip(models.Model):
    # id_user = models.ForeignKey('auth.User')
    no_rekam_medis = models.CharField(
        max_length = 50,
        unique = True)  
    waktu_saat_data_akan_diubah = models.DateTimeField(
        default=timezone.now)

# hanya bisa dicreate sama FO, dilihat oleh dokter
class antrian(models.Model):
    # karyawan_pendaftaran = models.ForeignKey('auth.User')
    dokter_tujuan = models.ForeignKey('Practitioner', null=True, on_delete=models.CASCADE)
    waktu = models.DateTimeField(
        default=timezone.now)
    no_antrian = models.AutoField(primary_key=True)
    
    # def __str__(self):
    #     return self.title
    def antrian_sekarang(self):
        no_antrian = self.no_antrian
        return self.no_antrian

# ++++++++++++++++++++++++++++++++++++++++++++
# ManyToManyField
class pasien_dari_dokter(models.Model):
    pasien = models.ForeignKey('Patient', related_name='pasiendokter', null=True, on_delete=models.CASCADE)
    dokter = models.ForeignKey('Practitioner', related_name='pasiendokter', null=True, on_delete=models.CASCADE)
    
    def __unicode__(self):
        # return "%s merupakan pasien %s" % (self.pasien, self.dokter)
        return "%s memiliki pasien %s" % (self.dokter, self.pasien)

# ++++++++++++++++++++++++++++++++++++++++++++

# class TimeStampedModel(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#     class Meta:
#         abstract = True

# ++++++++++++++++++++++++++++++++++++++++++++

class Condition(models.Model):
    patient = models.ForeignKey('Patient', null=True, on_delete=models.CASCADE)
    # id_pembuat = models.ForeignKey('auth.User')

    """Use to record detailed information about conditions, problems or
    diagnoses recognized by a clinician. There are many uses
    including: recording a diagnosis during an encounter; populating
    a problem list or a summary statement, such as a discharge
    summary.If the element is present, it must have either a @value,
    an @id, or extensionsEstimated or actual date or date-time the
    condition began, in the opinion of the clinician.The date or
    estimated date that the condition resolved or went into
    remission. This is called "abatement" because of the many
    overloaded connotations associated with "remission" or
    "resolution" - Conditions are never really resolved, but they
    can abate."""
    description = ("Detailed information about conditions, problems or diagnoses")

    # CATEGORY_CHOICES = (
    #     ('complaint', 'Keluhan'),
    #     ('symptom', 'Gejala'),
    #     ('finding', 'Penemuan'),
    #     ('diagnosis', 'Diagnosis'),
    # )
    CATEGORY_CHOICES = (
        ("complaint", 'Keluhan'),
        ("symptom", 'Gejala'),
        ("finding", 'Penemuan'),
        ("diagnosis", 'Diagnosis'),
    )

    # identifier = models.CharField( # External Ids for this condition
    #     help_text = "",
    #     max_length = 30,
    #     blank = False)
    # identifier = form 0..* (Identifier DONE)
    # patient  # Who has the condition? ref patient
    # encounter # Encounter when condition first asserted : ref encounter
    dateRecorded = models.DateTimeField( # When first entered
        auto_now = True,
        blank = False)
    code = models.CharField( # Identification of the condition, problem or diagnosis 
        # choices = Condition/Problem/Diagnosis Codes
        help_text = "kode",
        max_length = 20,
        blank = False)
    category = models.CharField(
        choices = CATEGORY_CHOICES,
        help_text = "",
        max_length = 20,
        blank = True)
# evidence = form 0..* (Evidence DONE)
    bodySite = models.CharField( # Anatomical location, if relevant | SNOMED CT Body Structures
        help_text = "",
        max_length = 245,
        blank = True)
    notes = models.TextField(blank=True)
    history = HistoricalRecords()

class DiagnosticReport(models.Model):
    # id_pembuat = models.ForeignKey('auth.User')
    description = ("A Diagnostic report - a combination of request information, atomic results, images, interpretation, as well as formatted reports")

    DIAGNOSTIC_REPORT_STATUS_CHOICES = (
        ('registered', mark_safe(u'<em></em> | ')), # The existence of the report is registered, but there is nothing yet available.
        ('partial', mark_safe(u'<em></em> | ')), # This is a partial (e.g. initial, interim or preliminary) report: data in the report may be incomplete or unverified.
        ('final', mark_safe(u'<em></em> | ')), # The report is complete and verified by an authorized person.
        ('corrected', mark_safe(u'<em></em> | ')), # The report has been modified subsequent to being Final, and is complete and verified by an authorized person. New content has been added, but existing content hasn't changed
        ('appended', mark_safe(u'<em></em> | ')), # The report has been modified subsequent to being Final, and is complete and verified by an authorized person. New content has been added, but existing content hasn't changed.
        ('cancelled', mark_safe(u'<em></em> | ')), # The report is unavailable because the measurement was not started or not completed (also sometimes called "aborted").
        ('entered-in-error', mark_safe(u'<em></em> | ')), # The report has been withdrawn following a previous final release.
    )
    # identifier = form 0..* (identifier DONE) Id for external references to this report
    status = models.CharField( #
        choices = DIAGNOSTIC_REPORT_STATUS_CHOICES,
        help_text = "",
        max_length = 20,
        blank = False)
    category= models.CharField( # Service category 
        # choices = Diagnostic Service Section Codes
        help_text = "",
        max_length = 20,
        blank = True)
    code = models.CharField( # Name/Code for this diagnostic report 
        # choices = LOINC Diagnostic Report 
        help_text = "",
        max_length = 20,
        blank = False)
    # subject = ref 1..1 (patient, location) The subject of the report, usually, but not always, the patient
    # encounter = ref 0..1 (encounter) Health care event when test ordered
# effective[x] :1..1(   Clinically Relevant time/time-period for report
    effectiveDateTime = models.DateTimeField( # 
        help_text = "",
        blank = False)
    # effectivePeriod = form 1..1 (Period DONE)
# )
    issued = models.DateTimeField( # DateTime this version was released
        default=timezone.now)
    # performer = ref 1..1 (practitioner) Responsible Diagnostic Service
    conclusion = models.CharField( # Clinical Interpretation of test results
        help_text = "",
        max_length = 20,
        blank = True)
    # codedDiagnosis = form 0..* (CodeableConcept DONE) Codes for the conclusion 
    #                  choices = SNOMED CT Clinical Findings
    # presentedForm = form 0..* (Attachment DONE) Entire report as issued
    history = HistoricalRecords()

class Encounter(models.Model):
    # id_pembuat = models.ForeignKey('auth.User')
    description = ("An interaction during which services are provided to the patient")

    ENCOUNTER_CLASS_CHOICES = ( # Classification of the encounter
        ('inpatient', mark_safe(u'<em>Rawat Inap</em> | ')), # An encounter during which the patient is hospitalized and stays overnight.
        ('outpatient', mark_safe(u'<em>Rawat Jalan</em> | ')), # An encounter during which the patient is not hospitalized overnight.
        ('ambulatory', mark_safe(u'<em></em> | ')), # An encounter where the patient visits the practitioner in his/her office, e.g. a G.P. visit.
        ('emergency', mark_safe(u'<em></em> | ')), #An encounter in the Emergency Care Department.
        ('home', mark_safe(u'<em>Rumah</em> | ')), # An encounter where the practitioner visits the patient at his/her home.
        ('field', mark_safe(u'<em>Lapangan</em> | ')), # An encounter taking place outside the regular environment for giving care.
        ('daytime', mark_safe(u'<em></em> | ')), # An encounter where the patient needs more prolonged treatment or investigations than outpatients, but who do not need to stay in the hospital overnight.
        ('virtual', mark_safe(u'<em>Virtual</em> | ')), # An encounter that takes place where the patient and practitioner do not physically meet but use electronic means for contact.
        ('other', mark_safe(u'<em>Lainnya</em> | ')), # Any other encounter type that is not described by one of the other values. Where this is used it is expected that an implementer will include an extension value to define what the actual other type is.
    )
    # identifier = form 0..* (Identifier DONE)   Identifier(s) by which this encounter is known
    Class = models.CharField( # inpatient | outpatient | ambulatory | emergency +
        choices = ENCOUNTER_CLASS_CHOICES,
        help_text = "",
        max_length = 15,
        blank = False)
    # patient = ref (patient) # The patient present at the encounter
    # participant = models.ForeignKey('auth.User')
    reason = models.CharField( # 0..* Reason the encounter takes place (code) 
        # choices = SNOMED 
        help_text = "",
        max_length = 20,
        blank = True)
    """Example
    Heart valve replacement (Details : {SNOMED CT code '34068001' = '34068001', given as 'Heart valve replacement'})"""
# location = 0..*( List of locations where the patient has been
    # location = ref (location) Location the encounter takes place
# )
    history = HistoricalRecords()
    created_date = models.DateTimeField(
        default=timezone.now)

# DONE 1 (POLI)
class HealthcareService(models.Model): #aka poli
    description = ("The details of a healthcare service available at a location")

    # identifier = models.CharField( # 0..* External identifiers for this item
    #     help_text = "",
    #     max_length = 20,
    #     blank = True)
    # identifier = form 0..* (Identifier DONE)
    serviceCategory = models.CharField( # 0..1 Broad category of service being performed or delivered
        help_text = "",
        max_length = 20,
        blank = True)
# serviceType : form 0..* (serviceType) Specific service delivered or performed
# location = ref 1..1 (Location) Location where service may be provided
    serviceName = models.CharField( # 0..1 Description of service as presented to a consumer while searching
        help_text = "",
        max_length = 20,
        blank = True)
    # telecom = form 0..* (ContactPoint DONE) Contacts related to the healthcare service
    history = HistoricalRecords()

class Location(models.Model):
    description = ("Details and position information for a physical place")
    # identifier = models.CharField( # Unique code or number identifying the location to its users
    #     help_text = "",
    #     max_length = 30,
    #     blank = True)
    # identifier = form 0..* (Identifier DONE)
    name = models.CharField( #  Name of the location as used by humans
        help_text = "",
        max_length = 150,
        blank = True)
    description = models.TextField( # Description of the location
        help_text = "Deskripsi lokasi",
        blank = True)
    history = HistoricalRecords()

class Identifier(models.Model):
    description = ("An identifier intended for computation")
    # id_pembuat = models.ForeignKey('auth.User')

    condition = models.ForeignKey('Condition', null=True, on_delete=models.CASCADE)
    diagnosticreport = models.ForeignKey('DiagnosticReport', null=True, on_delete=models.CASCADE)
    encounter = models.ForeignKey('Encounter', null=True, on_delete=models.CASCADE)
    healthcareservice = models.ForeignKey('HealthcareService', null=True, on_delete=models.CASCADE)
    # location = models.ForeignKey(Location)
    patient = models.ForeignKey('Patient', null=True, on_delete=models.CASCADE)
    practitioner = models.ForeignKey('Practitioner', null=True, on_delete=models.CASCADE)
    IDENTIFIER_TYPE_CODES_CHOICES = (
        ('UDI', 'Universal Device Identifier'),
        ('SNO', 'Serial Number'),
        ('SB', 'Social Beneficiary Identifier'),
        ('PLAC', 'Placer Identifier'),
        ('FILL', 'Filler Identifier'),
        ('KTP', 'KTP'), #tambahan
        ('DL', 'Surat Izin Mengemudi'),
        ('PPN', 'Nomor Paspor'),
        ('MR', 'Nomor Rekam Medis'),
        ('EN', 'Employer number'),
        ('MD', 'Medical License number'),
        ('DR', 'Donor Registration Number'),
    )

    Type = models.CharField( # Description of identifier 
        choices = IDENTIFIER_TYPE_CODES_CHOICES,
        # choices = Identifier Type in v2-tables.xml
        max_length = 100)
    Value = models.CharField( # The value that is unique
        primary_key=True,
        max_length = 65,
        )
    history = HistoricalRecords()

class Patient(models.Model):
    # id_pembuat = models.ForeignKey('auth.User')
    dokter = models.ManyToManyField('Practitioner', through='pasien_dari_dokter', related_name='para_pasien')
    # description = ("Demographics and other administrative information about an individual or animal receiving care or other health-related services.")  
    # condition = models.ForeignKey('Condition', on_delete=models.CASCADE)
    # encounter = models.ForeignKey('Encounter', on_delete=models.CASCADE)

    GENDER_CHOICES = (
        ('MALE', 'Laki-laki'),
        ('FEMALE', 'Perempuan'),
        ('OTHER', 'lainnya'),
        ('UNKNOWN', 'Tidak Diketahui'),
    )
    MARITAL_STATUS_CHOICES = (
    # ('Annulled', 'Mr.'),
        ('DIVORCED', 'Bercerai'),
    # ('Interlocutory', 'Ms.'),
        ('MARRIED', 'Menikah'),
        # ('POLYGAMOUS', 'Poligami'),
        ('NEVERMARRIED', 'Belum Menikah'),
    # ('Domestic partner', 'Pasangan Domestik'),
        ('WIDOWED', 'Duda/Janda'),
        ('UNKNOWN', 'Tidak Diketahui'),
    )
    LANGUAGE_CHOICES = (
        ('id', 'Indonesia'),
        ('en', 'Inggris'),
    )
    id_patient = models.AutoField(primary_key=True)
    # MedicalRecord_id = models.UUIDField(
    #     primary_key=True, 
    #     default=uuid.uuid4,
    #     unique=True,
    #     editable=False)
    # identifier = form 0..* (Identifier DONE) An identifier for this patient
    active = models.BooleanField( # Whether this patient's record is in active use
        default=True,
        verbose_name="Aktif", 
        help_text="Apakah rekam medis pasien masih aktif?",
        blank = False)
    # name = form 0..* (HumanName DONE) A name associated with the patient
    # telecom = form 0..* (ContactPoint DONE) A contact detail for the individual
    gender = models.CharField(
        # choices = AdministrativeGender
        choices=GENDER_CHOICES,
        max_length=10,
        verbose_name="Jenis Kelamin", 
        blank = True)
    birthDate = models.DateField(
        blank=True, 
        null = True, 
        auto_now=False, 
        auto_now_add=False)
# deceased[x] (0..1  Indicates if the individual is deceased or not
    deceasedBoolean = models.BooleanField( # 
        help_text = "",
        blank = False)
    deceasedDateTime = models.DateTimeField(
        blank=True,
        null=True, 
        )
# )
    # maritalStatus = form 0..1 (CodeableConcept DONE) Marital (civil) status of a patient 
    #                 choice = Marital Status Codes
    maritalStatus = models.CharField(
    choices = MARITAL_STATUS_CHOICES,
    max_length = 20,
    blank = True)
    # photo = form 0..* (Attachment DONE) Image of the patient
    language = models.CharField(
        choices = LANGUAGE_CHOICES,
        help_text="Bahasa yang dikuasai",
        blank=False,
        max_length=5)
    # Contact = form 0..*(Contact)
    created_date = models.DateTimeField(
        default=timezone.now)
    # edited_date = models.DateTimeField(
    #     blank=True, null=True)

    # def create(self):
    #     self.created_date = timezone.now()
    #     self.save()

    # def __str__(self):
    #     return self.name
    history = HistoricalRecords()

    def __str__(self):
        return self.id_patient


# =========================================== #
# DONE 1
class Practitioner(models.Model):
    """Doctor : Typically a licensed person who is providing or performing 
    care related to the event, generally a physician. The key 
    distinction between doctor and practitioner is with regards 
    to their role, not the licensing. The doctor is the human who 
    actually performed the work. The practitioner is the human or 
    organization that is responsible for the work."""
    
    # id_pembuat = models.ForeignKey('auth.User')
    description = ("A person with a formal responsibility in the provisioning of healthcare or related services")

    # identifier = form 0..* (Identifier DONE) A identifier for the person as this agent
    # name = form 0..1 (HumanName DONE) A name associated with the person
    # practitionerrole = form 0..*(PractitionerRole)

# =========================================== #
# DONE 1
class PractitionerRole(models.Model):
    # id_pembuat = models.ForeignKey('auth.User')
    description = ("Roles/organizations the practitioner is associated with")
    practitioner = models.ForeignKey('Practitioner', null=True, on_delete=models.CASCADE)

    ROLE_CHOICES = (
        ('doctor', 'Dokter'), # Doctor
        ('nurse', 'Perawat'), # Nurse
        ('pharmacist', 'Apoteker'), # Pharmacist
        ('researcher', 'Peneliti'), # Researcher
        ('teacher', 'Pengajar'), # Teacher/educator
        ('ict', 'Profesional ICT'), # ICT professional
    )
    SPECIALITY_CHOICES = (
        ('cardio', 'Ahli Jantung'), # Cardiologist
        ('dent', 'Dokter Gigi'), # Dentist
        ('dietary', 'Konsultan Diet'), # Dietary consultant 
        ('midw', 'Bidan'), # Midwife
        ('sysarch', 'Ahli Sistem'), # Systems architect
    )
    role = models.CharField(
        choices = ROLE_CHOICES,
        max_length = 20,
        blank = True)
    specialty = models.CharField(
        choices = SPECIALITY_CHOICES,
        max_length = 20,
        blank = True)

# =========================================== #
# DONE 1
class Address(models.Model):
    # id_pembuat = models.ForeignKey('auth.User')
    description = ("A postal address")
    
    patient = models.ForeignKey('Patient', null=True, on_delete=models.CASCADE)
    practitioner = models.ForeignKey('Practitioner', null=True, on_delete=models.CASCADE)
    # USE_CHOICES = (
    #     ('HOME', 'Rumah'),
    #     ('WORK', 'Kantor'),
    #     ('TEMP', 'Sementara'),
    #     ('OLD', 'Lama'),
    # )
    TYPE_CHOICES = (
        ('POSTAL', 'Postal'),
        ('PHYSICAL', 'Fisik'),
        ('BOTH', 'Postal dan Fisik'),
    )

    # Use = models.CharField(
    #     # choices = AddressUse
    #     choices=USE_CHOICES,
    #     help_text="Tujuan dari alamat",
    #     blank=True,
    #     max_length=10)
    Type = models.CharField(
        # choices = AddressType
        choices=TYPE_CHOICES, 
        help_text="Tipe alamat",
        blank=True,
        max_length=10)
    text = models.CharField( # Text representation of the address
        help_text="Alamat Lengkap",
        max_length=200,
        blank=True)
    line = models.CharField( # 0..* Street name, number, direction & P.O. Box etc.
        help_text="Nama jalan, nomor, P.O. Box, dan lainnya",
        max_length=200,
        blank=True)
    city = models.CharField( # Name of city, town etc.
        help_text="Nama kota",
        max_length=100,
        blank=True)
    district = models.CharField( # District name (aka county)
        help_text="District name (aka county)",
        max_length=100,
        blank=True)
    state = models.CharField( # Sub-unit of country (abbreviations ok)
        help_text="Sub-unit of country (abbreviations ok)",
        max_length=100,
        blank=True)
    postalCode = models.CharField( # Postal code for area
        help_text="Kode Pos",
        max_length=20,
        blank=True)
    country = models.CharField( # Country (can be ISO 3166 3 letter code)
        help_text="Negara",
        max_length=150,
        blank=True)
    history = HistoricalRecords()
    # def __str__(self):
    #     return self.Type

# =========================================== #
# DONE 1 ^^
class ServiceType(models.Model):
    description = ("Specific service delivered or performed") 
    healthcareservice = models.ForeignKey('HealthcareService', null=True, on_delete=models.CASCADE)
    Type = models.CharField( # 1..1     Type of service delivered or performed 
        # choices = Practice Setting Code Value Set in valueset.xml
        help_text = "",
        max_length = 20,
        blank = False)

# =========================================== #
# DONE 1
class Quantity(models.Model):
    description = ("A measured or measurable amount")
    # ratio = models.ForeignKey(Ratio)

    COMPARATOR_CHOICES = (
        ('less', '<'),
        ('lessequal', '<='),
        ('moreequal', '>='),
        ('more', '>')
    )
    Value = models.DecimalField(
        blank = True,
        max_digits = 60,
        decimal_places = 3) # Numerical value (with implicit precision)
    comparator = models.CharField( 
        choices = COMPARATOR_CHOICES,
        max_length = 9,
        blank=True)
    unit = models.CharField(  #Unit representation
        max_length = 200,
        blank=True) 

class HumanName(models.Model):
    # id_pembuat = models.ForeignKey('auth.User')
    description = ("Name of a human - parts and usage")
    patient = models.ForeignKey('Patient', null=True, on_delete=models.CASCADE)
    practitioner = models.ForeignKey('Practitioner', null=True, on_delete=models.CASCADE)

    text = models.CharField(
        help_text = "Nama Lengkap", # Text representation of the full name
        max_length=245) 
    family = models.CharField(
        help_text = "Nama keluarga", # Family name (often called 'Surname')
        max_length=50)
    given = models.CharField( # Given names (not always 'first'). Includes middle names
        help_text = "Nama pemberian/nama depan termasuk nama tengah (jika ada)",
        max_length=50)
    # def __str__(self):
    #     return self.text

class ContactPoint(models.Model):
    # id_pembuat = models.ForeignKey('auth.User')
    description = ("Details of a Technology mediated contact point (phone, fax, email, etc.) ")
    """A system is required if a value is provided."""
    patient = models.ForeignKey('Patient')
    practitioner = models.ForeignKey('Practitioner', null=True, on_delete=models.CASCADE)
    healthcareservice = models.ForeignKey('HealthcareService', null=True, on_delete=models.CASCADE)

    SYSTEM_CHOICES = (
        ('phone', 'Rumah'),
        ('fax', 'Kantor'),
        ('email', 'Sementara'),
        ('pager', 'Lama'),
        ('other', 'Lama'),
    )

    system = models.CharField(
        # choices = ContactPointSystem
        choices=SYSTEM_CHOICES,
        help_text="Jenis sistem",
        blank=True,
        max_length=10)
    Value = models.CharField( #The actual contact point details
        blank=True,
        max_length= 65)
    history = HistoricalRecords()
    # def __str__(self):
    #     return self.system
   
class Attachment(models.Model):
    description = ("Content in a format defined elsewhere. If the Attachment has data, it SHALL have a contentType")
    
    DiagnosticReport = models.ForeignKey('DiagnosticReport', null=True, on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', null=True, on_delete=models.CASCADE)

    contentType = models.CharField( # Mime type of the content, with charset etc. 
        max_length = 200,
        blank = True)
    # data = models.FileField( # Data inline, base64ed
        # upload_to = 'uploads/',
        # size = 
        # )
    # url = model.URLField(max_length=200)
    url = models.CharField( #Uri where the data can be found
        max_length=200,
        blank=True) 
    # size = data.size #(Number of bytes of content (if url provided))
    # Hash = models.FileField() # Hash of the data (sha-1, base64ed)
    title = models.CharField( # Label to display in place of the data
        max_length=200,
        blank=True) 
    creation = models.DateTimeField(auto_now=True) # Date attachment was first created
#ref : https://docs.djangoproject.com/en/1.9/ref/models/fields/#null
#ref : https://docs.djangoproject.com/en/1.9/ref/files/file/#django.core.files.File.size

class Evidence(models.Model):
    # id_pembuat = models.ForeignKey('auth.User')
    condition = models.ForeignKey('Condition', null=True, on_delete=models.CASCADE)
    description = ("Supporting evidence. Evidence SHALL have code or details")

    code = models.CharField( # Manifestation/symptom 
        help_text = "",
        max_length = 20,
        blank = True)
    detail = models.TextField(blank=True) # Supporting information found elsewhere
    history = HistoricalRecords()
    # def __str__(self):
    #     return self.code
        
class Period(models.Model):
    description = ("Time range defined by start and end date/time. If present, start SHALL have a lower value than end")
    
    address = models.ForeignKey('Address', null=True, on_delete=models.CASCADE)
    condition = models.ForeignKey('Condition', null=True, on_delete=models.CASCADE)
    contactpoint = models.ForeignKey('ContactPoint', null=True, on_delete=models.CASCADE)
    DiagnosticReport = models.ForeignKey('DiagnosticReport', null=True, on_delete=models.CASCADE)
    encounter = models.ForeignKey('Encounter', null=True, on_delete=models.CASCADE) 
    identifier = models.ForeignKey('Identifier', null=True, on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', null=True, on_delete=models.CASCADE)
    practitioner = models.ForeignKey('Practitioner', null=True, on_delete=models.CASCADE)
    practitionerrole = models.ForeignKey('PractitionerRole', null=True, on_delete=models.CASCADE)

    start = models.DateTimeField( # Starting time with inclusive boundary
        blank = True)
    end = models.DateTimeField( # End time with inclusive boundary, if not ongoing
        blank = True)
    history = HistoricalRecords()

class Reference(models.Model):
    description = ("A reference from one resource to another")

    condition = models.ForeignKey('Condition', null=True, on_delete=models.CASCADE)
    diagnosticreport = models.ForeignKey('DiagnosticReport', null=True, on_delete=models.CASCADE)
    encounter = models.ForeignKey('Encounter', null=True, on_delete=models.CASCADE)
    healthcareservice = models.ForeignKey('HealthcareService', null=True, on_delete=models.CASCADE)
    location = models.ForeignKey('Location', null=True, on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', null=True, on_delete=models.CASCADE)

    reference = models.TextField( # 0..1 Relative, internal or absolute URL reference
        help_text = "",
        default='',
        blank = True)
    display = models.CharField( # 0..1 Text alternative for the resource
        help_text = "",
        max_length = 245,
        blank = True)
    history = HistoricalRecords()

class CodeableConcept(models.Model):
    description = ("Concept - reference to a terminology or just text")
    
    patient = models.ForeignKey('Patient', null=True, on_delete=models.CASCADE)
    practitioner = models.ForeignKey('Practitioner', null=True, on_delete=models.CASCADE)
    practitionerrole = models.ForeignKey('PractitionerRole', null=True, on_delete=models.CASCADE)
    diagnosticreport = models.ForeignKey('DiagnosticReport', null=True, on_delete=models.CASCADE)

    # coding = form 0..* (Coding DONE) Code defined by a terminology system
    text = models.CharField( # 
        help_text = "",
        max_length = 245,
        blank = True)
    history = HistoricalRecords()

class Coding(models.Model):
    description = ("A reference to a code defined by a terminology system")
    codeableconcept = models.ForeignKey('CodeableConcept', null=True, on_delete=models.CASCADE)    

    system = models.CharField( # Identity of the terminology system
        help_text = "",
        max_length = 200,
        blank = True)
    version = models.CharField( #   Version of the system - if relevant
        help_text = "",
        max_length = 200,
        blank = True)
    code = models.CharField( # Symbol in syntax defined by the system
        help_text = "",
        max_length = 200,
        blank = True)
    display = models.CharField( # Representation defined by the system
        help_text = "",
        max_length = 245,
        blank = True)
    userSelected= models.BooleanField( # If this coding was chosen directly by the user
        help_text = "")
    history = HistoricalRecords()