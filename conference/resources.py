from import_export import resources, fields
from .models import AbstractSubmission

class AbstractSubmissionResource(resources.ModelResource):
    phone = fields.Field(column_name='Phone Number')

    # CoAuthor 1
    coauthor1_name = fields.Field(column_name='CoAuthor1 Name')
    coauthor1_email = fields.Field(column_name='CoAuthor1 Email')
    coauthor1_designation = fields.Field(column_name='CoAuthor1 Designation')
    coauthor1_affiliation = fields.Field(column_name='CoAuthor1 Affiliation')

    # CoAuthor 2
    coauthor2_name = fields.Field(column_name='CoAuthor2 Name')
    coauthor2_email = fields.Field(column_name='CoAuthor2 Email')
    coauthor2_designation = fields.Field(column_name='CoAuthor2 Designation')
    coauthor2_affiliation = fields.Field(column_name='CoAuthor2 Affiliation')

    # CoAuthor 3
    coauthor3_name = fields.Field(column_name='CoAuthor3 Name')
    coauthor3_email = fields.Field(column_name='CoAuthor3 Email')
    coauthor3_designation = fields.Field(column_name='CoAuthor3 Designation')
    coauthor3_affiliation = fields.Field(column_name='CoAuthor3 Affiliation')

    # CoAuthor 4
    coauthor4_name = fields.Field(column_name='CoAuthor4 Name')
    coauthor4_email = fields.Field(column_name='CoAuthor4 Email')
    coauthor4_designation = fields.Field(column_name='CoAuthor4 Designation')
    coauthor4_affiliation = fields.Field(column_name='CoAuthor4 Affiliation')

    # CoAuthor 5
    coauthor5_name = fields.Field(column_name='CoAuthor5 Name')
    coauthor5_email = fields.Field(column_name='CoAuthor5 Email')
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

    def dehydrate_phone(self, obj):
        return obj.user.userprofile.phone if hasattr(obj.user, 'userprofile') else ''

    def dehydrate_coauthor1_name(self, obj): return obj.get_coauthor1_name()
    def dehydrate_coauthor1_email(self, obj): return obj.get_coauthor1_email()
    def dehydrate_coauthor1_designation(self, obj): return obj.get_coauthor1_designation()
    def dehydrate_coauthor1_affiliation(self, obj): return obj.get_coauthor1_affiliation()

    def dehydrate_coauthor2_name(self, obj): return obj.get_coauthor2_name()
    def dehydrate_coauthor2_email(self, obj): return obj.get_coauthor2_email()
    def dehydrate_coauthor2_designation(self, obj): return obj.get_coauthor2_designation()
    def dehydrate_coauthor2_affiliation(self, obj): return obj.get_coauthor2_affiliation()

    def dehydrate_coauthor3_name(self, obj): return obj.get_coauthor3_name()
    def dehydrate_coauthor3_email(self, obj): return obj.get_coauthor3_email()
    def dehydrate_coauthor3_designation(self, obj): return obj.get_coauthor3_designation()
    def dehydrate_coauthor3_affiliation(self, obj): return obj.get_coauthor3_affiliation()

    def dehydrate_coauthor4_name(self, obj): return obj.get_coauthor4_name()
    def dehydrate_coauthor4_email(self, obj): return obj.get_coauthor4_email()
    def dehydrate_coauthor4_designation(self, obj): return obj.get_coauthor4_designation()
    def dehydrate_coauthor4_affiliation(self, obj): return obj.get_coauthor4_affiliation()

    def dehydrate_coauthor5_name(self, obj): return obj.get_coauthor5_name()
    def dehydrate_coauthor5_email(self, obj): return obj.get_coauthor5_email()
    def dehydrate_coauthor5_designation(self, obj): return obj.get_coauthor5_designation()
    def dehydrate_coauthor5_affiliation(self, obj): return obj.get_coauthor5_affiliation()
