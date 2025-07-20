from import_export import resources, fields
from .models import AbstractSubmission

class AbstractSubmissionResource(resources.ModelResource):
    phone = fields.Field(
        column_name='Phone Number',
        attribute='user__profile__phone',
    )

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
            'paper_id', 'title', 'name', 'email', 'phone', 'institute', 'designation',
            'keywords', 'status', 'submitted_on',
            'coauthor1_name', 'coauthor1_email', 'coauthor1_designation', 'coauthor1_affiliation',
            'coauthor2_name', 'coauthor2_email', 'coauthor2_designation', 'coauthor2_affiliation',
            'coauthor3_name', 'coauthor3_email', 'coauthor3_designation', 'coauthor3_affiliation',
            'coauthor4_name', 'coauthor4_email', 'coauthor4_designation', 'coauthor4_affiliation',
            'coauthor5_name', 'coauthor5_email', 'coauthor5_designation', 'coauthor5_affiliation',
        )

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


from import_export import resources, fields
from .models import FinalRegistration, FinalParticipant

class FinalRegistrationResource(resources.ModelResource):
    paper_id          = fields.Field(column_name='Paper ID', attribute='submission__paper_id')
    main_author_name  = fields.Field(column_name='Main Author', attribute='author_name')
    main_author_email = fields.Field(column_name='Main Author Email',
                                     attribute='submission__user__email')
    main_author_institute = fields.Field(column_name='Main Author Institute',
                                         attribute='submission__institute')
    main_author_designation = fields.Field(column_name='Main Author Designation',
                                           attribute='author_designation')
    author_contact    = fields.Field(column_name='Author Contact', attribute='author_contact')
    author_address    = fields.Field(column_name='Author Address', attribute='author_address')
    author_gender     = fields.Field(column_name='Author Gender', attribute='author_gender')
    author_mode       = fields.Field(column_name='Author Mode', attribute='author_mode')

    coauthors = fields.Field(column_name='Co-Authors')
    visitors  = fields.Field(column_name='Visitors')
    title = fields.Field(column_name='Title', attribute='submission__title')
    selected_theme = fields.Field(column_name='Selected Theme', attribute='selected_theme')


    total_amount      = fields.Field(column_name='Total Amount', attribute='total_amount')

    class Meta:
        model = FinalRegistration
        fields = (
        'paper_id',
        'title',
        'selected_theme',
        'main_author_name', 'main_author_email', 'main_author_institute',
        'main_author_designation', 'author_contact','author_address',
        'author_gender','author_mode',
        'coauthors','visitors',
        'total_amount',
        )

        export_order = fields

    def dehydrate_coauthors(self, reg):
        parts = []
        for p in reg.participants.filter(role='CoAuthor'):
            parts.append(
              f"{p.name} ({p.email}, {p.contact}, {p.mode})"
            )
        return "; ".join(parts) or "—"

    def dehydrate_visitors(self, reg):
        parts = []
        for p in reg.participants.filter(role='Visitor'):
            parts.append(
              f"{p.name} ({p.email or 'N/A'}, {p.contact}, {p.mode})"
            )
        return "; ".join(parts) or "—"
