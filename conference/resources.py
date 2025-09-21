from import_export import resources, fields
from .models import AbstractSubmission

from import_export import resources, fields
from .models import AbstractSubmission

class AbstractSubmissionResource(resources.ModelResource):
    # Pull phone directly via the relation chain user → profile → phone
    phone = fields.Field(
        column_name='Phone Number',
        attribute='user__profile__phone',
    )
    mode_of_participation = fields.Field(
    column_name='Mode of Participation',
    attribute='mode_of_participation'
    )
    full_paper_url = fields.Field(column_name="Full Paper URL")
    full_paper_filename = fields.Field(column_name="Full Paper Filename")



    # CoAuthor 1
    coauthor1_name        = fields.Field(column_name='CoAuthor1 Name')
    coauthor1_email       = fields.Field(column_name='CoAuthor1 Email')
    coauthor1_designation = fields.Field(column_name='CoAuthor1 Designation')
    coauthor1_affiliation = fields.Field(column_name='CoAuthor1 Affiliation')

    # CoAuthor 2
    coauthor2_name        = fields.Field(column_name='CoAuthor2 Name')
    coauthor2_email       = fields.Field(column_name='CoAuthor2 Email')
    coauthor2_designation = fields.Field(column_name='CoAuthor2 Designation')
    coauthor2_affiliation = fields.Field(column_name='CoAuthor2 Affiliation')

    # CoAuthor 3
    coauthor3_name        = fields.Field(column_name='CoAuthor3 Name')
    coauthor3_email       = fields.Field(column_name='CoAuthor3 Email')
    coauthor3_designation = fields.Field(column_name='CoAuthor3 Designation')
    coauthor3_affiliation = fields.Field(column_name='CoAuthor3 Affiliation')

    # CoAuthor 4
    coauthor4_name        = fields.Field(column_name='CoAuthor4 Name')
    coauthor4_email       = fields.Field(column_name='CoAuthor4 Email')
    coauthor4_designation = fields.Field(column_name='CoAuthor4 Designation')
    coauthor4_affiliation = fields.Field(column_name='CoAuthor4 Affiliation')

    # CoAuthor 5
    coauthor5_name        = fields.Field(column_name='CoAuthor5 Name')
    coauthor5_email       = fields.Field(column_name='CoAuthor5 Email')
    coauthor5_designation = fields.Field(column_name='CoAuthor5 Designation')
    coauthor5_affiliation = fields.Field(column_name='CoAuthor5 Affiliation')

    class Meta:
        model = AbstractSubmission
        fields = (
            'paper_id', 'title','mode_of_participation', 'name', 'email', 'phone', 'institute', 'designation',
            'keywords', 'status', 'submitted_on',
            'coauthor1_name', 'coauthor1_email', 'coauthor1_designation', 'coauthor1_affiliation',
            'coauthor2_name', 'coauthor2_email', 'coauthor2_designation', 'coauthor2_affiliation',
            'coauthor3_name', 'coauthor3_email', 'coauthor3_designation', 'coauthor3_affiliation',
            'coauthor4_name', 'coauthor4_email', 'coauthor4_designation', 'coauthor4_affiliation',
            'coauthor5_name', 'coauthor5_email', 'coauthor5_designation', 'coauthor5_affiliation',
            'full_paper_url', 'full_paper_filename',
        )

    # No need for a dehydrate_phone method anymore,
    # django-import-export will pull from user__profile__phone automatically.

    def dehydrate_coauthor1_name(self, obj):        return obj.get_coauthor1_name()
    def dehydrate_coauthor1_email(self, obj):       return obj.get_coauthor1_email()
    def dehydrate_coauthor1_designation(self, obj): return obj.get_coauthor1_designation()
    def dehydrate_coauthor1_affiliation(self, obj): return obj.get_coauthor1_affiliation()

    def dehydrate_coauthor2_name(self, obj):        return obj.get_coauthor2_name()
    def dehydrate_coauthor2_email(self, obj):       return obj.get_coauthor2_email()
    def dehydrate_coauthor2_designation(self, obj): return obj.get_coauthor2_designation()
    def dehydrate_coauthor2_affiliation(self, obj): return obj.get_coauthor2_affiliation()

    def dehydrate_coauthor3_name(self, obj):        return obj.get_coauthor3_name()
    def dehydrate_coauthor3_email(self, obj):       return obj.get_coauthor3_email()
    def dehydrate_coauthor3_designation(self, obj): return obj.get_coauthor3_designation()
    def dehydrate_coauthor3_affiliation(self, obj): return obj.get_coauthor3_affiliation()

    def dehydrate_coauthor4_name(self, obj):        return obj.get_coauthor4_name()
    def dehydrate_coauthor4_email(self, obj):       return obj.get_coauthor4_email()
    def dehydrate_coauthor4_designation(self, obj): return obj.get_coauthor4_designation()
    def dehydrate_coauthor4_affiliation(self, obj): return obj.get_coauthor4_affiliation()

    def dehydrate_coauthor5_name(self, obj):        return obj.get_coauthor5_name()
    def dehydrate_coauthor5_email(self, obj):       return obj.get_coauthor5_email()
    def dehydrate_coauthor5_designation(self, obj): return obj.get_coauthor5_designation()
    def dehydrate_coauthor5_affiliation(self, obj): return obj.get_coauthor5_affiliation()
    def dehydrate_full_paper_url(self, obj):
        try:
            return obj.full_paper.url if obj.full_paper else ""
        except Exception:
            return ""

    def dehydrate_full_paper_filename(self, obj):
        import os, urllib.parse
        url = self.dehydrate_full_paper_url(obj)
        if not url:
            return ""
        path = urllib.parse.urlsplit(url).path
        return urllib.parse.unquote(os.path.basename(path))

# conference/resources.pyfrom import_export import resources, fields
from .models import FinalRegistration

class FinalRegistrationResource(resources.ModelResource):
    paper_id               = fields.Field(column_name='Paper ID', attribute='submission__paper_id')
    title                  = fields.Field(column_name='Title', attribute='submission__title')
    selected_theme         = fields.Field(column_name='Selected Theme')  # dehydrate below will supply readable label

    main_author_name       = fields.Field(column_name='Main Author', attribute='author_name')
    main_author_email      = fields.Field(column_name='Main Author Email', attribute='submission__user__email')
    main_author_institute  = fields.Field(column_name='Main Author Institute', attribute='submission__institute')
    main_author_designation= fields.Field(column_name='Main Author Designation', attribute='author_designation')

    author_contact         = fields.Field(column_name='Author Contact', attribute='author_contact')
    author_address         = fields.Field(column_name='Author Address', attribute='author_address')
    author_gender          = fields.Field(column_name='Author Gender', attribute='author_gender')
    author_mode            = fields.Field(column_name='Author Mode', attribute='author_mode')

    coauthors              = fields.Field(column_name='Co-Authors')
    visitors               = fields.Field(column_name='Visitors')
    presenter_name = fields.Field(column_name='Presenter Name', attribute='presenter_name')

    total_amount           = fields.Field(column_name='Total Amount', attribute='total_amount')

    class Meta:
        model = FinalRegistration
        # explicitly list/export fields in the order you want
        fields = (
            'paper_id', 'title', 'selected_theme',
            'main_author_name', 'main_author_email', 'main_author_institute', 'main_author_designation',
            'author_contact', 'author_address', 'author_gender', 'author_mode',
            'coauthors', 'visitors', 'presenter_name',
            'total_amount',
        )
        export_order = fields  # <-- THIS line below is fine only because we've defined a local variable `fields` above
        # If you prefer an explicit tuple:
        # export_order = (
        #    'paper_id', 'title', 'selected_theme', 'main_author_name', ... ,'total_amount'
        # )

    def dehydrate_selected_theme(self, reg):
        # For a choices CharField, this returns the display label.
        if hasattr(reg, 'get_selected_theme_display'):
            return reg.get_selected_theme_display() or ''
        # Fallback just in case it's None or plain text
        return str(reg.selected_theme or '')

    def dehydrate_coauthors(self, reg):
        parts = []
        for p in reg.participants.filter(role='CoAuthor'):
            parts.append(f"{p.name} ({p.email or 'N/A'}, {p.contact}, {p.mode})")
        return "; ".join(parts) or "—"

    def dehydrate_visitors(self, reg):
        parts = []
        for p in reg.participants.filter(role='Visitor'):
            parts.append(f"{p.name} ({p.email or 'N/A'}, {p.contact}, {p.mode})")
        return "; ".join(parts) or "—"


from import_export import resources, fields
from .models import VisitorRegistration, AdditionalVisitor

class VisitorRegistrationResource(resources.ModelResource):
    # Main visitor fields
    name         = fields.Field(column_name='Name', attribute='name')
    email        = fields.Field(column_name='Email', attribute='email')
    contact      = fields.Field(column_name='Contact', attribute='contact')
    address      = fields.Field(column_name='Address', attribute='address')
    id_proof_type = fields.Field(column_name='ID Proof Type', attribute='id_proof_type')
    id_proof_file = fields.Field(column_name='ID Proof File', attribute='id_proof_file')
    status        = fields.Field(column_name='Status', attribute='status')
    timestamp     = fields.Field(column_name='Submitted At', attribute='timestamp')

    # Additional visitor 1
    other_1_name     = fields.Field(column_name='Visitor 1 Name')
    other_1_contact  = fields.Field(column_name='Visitor 1 Contact')
    other_1_id_type  = fields.Field(column_name='Visitor 1 ID Type')
    other_1_id_file  = fields.Field(column_name='Visitor 1 ID File')

    # Additional visitor 2
    other_2_name     = fields.Field(column_name='Visitor 2 Name')
    other_2_contact  = fields.Field(column_name='Visitor 2 Contact')
    other_2_id_type  = fields.Field(column_name='Visitor 2 ID Type')
    other_2_id_file  = fields.Field(column_name='Visitor 2 ID File')

    # Additional visitor 3
    other_3_name     = fields.Field(column_name='Visitor 3 Name')
    other_3_contact  = fields.Field(column_name='Visitor 3 Contact')
    other_3_id_type  = fields.Field(column_name='Visitor 3 ID Type')
    other_3_id_file  = fields.Field(column_name='Visitor 3 ID File')

    class Meta:
        model = VisitorRegistration
        export_order = [
            'name', 'email', 'contact', 'address',
            'id_proof_type', 'id_proof_file',
            'status', 'timestamp',
            'other_1_name', 'other_1_contact', 'other_1_id_type', 'other_1_id_file',
            'other_2_name', 'other_2_contact', 'other_2_id_type', 'other_2_id_file',
            'other_3_name', 'other_3_contact', 'other_3_id_type', 'other_3_id_file',
        ]

    def dehydrate_other_1_name(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[0].name if len(visitors) > 0 else ''

    def dehydrate_other_1_contact(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[0].contact if len(visitors) > 0 else ''

    def dehydrate_other_1_id_type(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[0].id_proof_type if len(visitors) > 0 else ''

    def dehydrate_other_1_id_file(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[0].id_proof_file.url if len(visitors) > 0 and visitors[0].id_proof_file else ''

    def dehydrate_other_2_name(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[1].name if len(visitors) > 1 else ''

    def dehydrate_other_2_contact(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[1].contact if len(visitors) > 1 else ''

    def dehydrate_other_2_id_type(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[1].id_proof_type if len(visitors) > 1 else ''

    def dehydrate_other_2_id_file(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[1].id_proof_file.url if len(visitors) > 1 and visitors[1].id_proof_file else ''

    def dehydrate_other_3_name(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[2].name if len(visitors) > 2 else ''

    def dehydrate_other_3_contact(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[2].contact if len(visitors) > 2 else ''

    def dehydrate_other_3_id_type(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[2].id_proof_type if len(visitors) > 2 else ''

    def dehydrate_other_3_id_file(self, obj):
        visitors = obj.additionalvisitor_set.all()
        return visitors[2].id_proof_file.url if len(visitors) > 2 and visitors[2].id_proof_file else ''
