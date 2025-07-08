from django import forms
from django.contrib import admin
from import_export.admin import ExportMixin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages

from .models import AbstractSubmission, CoAuthor
from .resources import AbstractSubmissionResource
from .forms import FullPaperUploadForm


# Inline form for co-authors
class CoAuthorInline(admin.TabularInline):
    model = CoAuthor
    extra = 0
    readonly_fields = ('first_name', 'last_name', 'email', 'affiliation', 'designation')


# Optional admin form for full paper upload
class FullPaperUploadForm(forms.ModelForm):
    class Meta:
        model = AbstractSubmission
        fields = ['full_paper']


# Admin for AbstractSubmission
@admin.register(AbstractSubmission)
class AbstractSubmissionAdmin(ExportMixin, admin.ModelAdmin):
    form = FullPaperUploadForm
    resource_class = AbstractSubmissionResource

    list_display = (
        'paper_id', 'title', 'corresponding_author_name', 'corresponding_author_email',
        'main_author_phone','corresponding_author_affiliation', 'corresponding_author_designation',
        'status', 'submitted_on', 'abstract_file_link', 'actions_column'
    )
    ordering = ('paper_id',)  # ✅ Default ordering
    list_filter = ('status', 'institute', 'designation')
    search_fields = ('paper_id', 'name', 'user__email', 'keywords')
    
    list_filter = ('status', 'institute', 'designation')
    search_fields = ('paper_id', 'name', 'user__email', 'keywords')
    inlines = [CoAuthorInline]
    readonly_fields = ('paper_id', 'submitted_on', 'abstract_file_link')
    list_editable = ('status',)
    actions = ['approve_selected', 'reject_selected']

    def corresponding_author_name(self, obj):
        return obj.name
    corresponding_author_name.short_description = "Main Author"

    def main_author_phone(self, obj):
        return obj.user.userprofile.phone
    main_author_phone.short_description = "Phone"


    def corresponding_author_email(self, obj):
        return obj.user.email if obj.user and obj.user.email else "-"
    corresponding_author_email.short_description = "Email"

    def corresponding_author_affiliation(self, obj):
        return obj.institute if obj.institute else "-"
    corresponding_author_affiliation.short_description = "Affiliation"

    def corresponding_author_designation(self, obj):
        return obj.designation if obj.designation else "-"
    corresponding_author_designation.short_description = "Designation"

    def abstract_file_link(self, obj):
        if obj.abstract_file:
            return format_html('<a href="{}" target="_blank">View</a>', obj.abstract_file.url)
        return "No File"
    abstract_file_link.short_description = "Abstract File"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:pk>/', self.admin_site.admin_view(self.approve_abstract), name='abstract-approve'),
            path('reject/<int:pk>/', self.admin_site.admin_view(self.reject_abstract), name='abstract-reject'),
        ]
        return custom_urls + urls

    def actions_column(self, obj):
        if obj.status == 'PENDING':
            return format_html(
                '<a class="button" href="{}">Approve</a>&nbsp;'
                '<a class="button" href="{}" style="color:red;">Reject</a>',
                f'approve/{obj.pk}/',
                f'reject/{obj.pk}/'
            )
        return "-"
    actions_column.short_description = 'Actions'

    def approve_selected(self, request, queryset):
        updated = 0
        for obj in queryset:
            if obj.status != 'APPROVED':
                obj.status = 'APPROVED'
                obj.save()
                self.send_approval_email(obj)
                updated += 1
        self.message_user(request, f"{updated} abstracts approved and email sent.")
    approve_selected.short_description = "Approve selected abstracts"

    def reject_selected(self, request, queryset):
        updated = 0
        for obj in queryset:
            if obj.status != 'REJECTED':
                obj.status = 'REJECTED'
                obj.save()
                self.send_rejection_email(obj)
                updated += 1
        self.message_user(request, f"{updated} abstracts rejected and email sent.")
    reject_selected.short_description = "Reject selected abstracts"

    def approve_abstract(self, request, pk):
        obj = get_object_or_404(AbstractSubmission, pk=pk)
        if obj.status != 'APPROVED':
            obj.status = 'APPROVED'
            obj.save()
            self.send_approval_email(obj)
            self.message_user(request, f"'{obj.title}' approved and email sent.")
        return redirect('admin:conference_abstractsubmission_changelist')

    def reject_abstract(self, request, pk):
        obj = get_object_or_404(AbstractSubmission, pk=pk)
        if obj.status != 'REJECTED':
            obj.status = 'REJECTED'
            obj.save()
            self.send_rejection_email(obj)
            self.message_user(request, f"'{obj.title}' rejected and email sent.")
        return redirect('admin:conference_abstractsubmission_changelist')

    def send_approval_email(self, obj):
        send_mail(
            subject="Abstract Approved – Conf2025",
            message=(
                f"Dear {obj.user.first_name},\n\n"
                f"Your abstract titled \"{obj.title}\" has been APPROVED.\n"
                "You can now upload your final paper and proceed to payment.\n"
                "Login to your profile here: http://127.0.0.1:8000/profile/\n\n"
                "Regards,\nConf2025 Secretariat"
            ),
            from_email=None,
            recipient_list=[obj.user.email],
            fail_silently=False,
        )

    def send_rejection_email(self, obj):
        send_mail(
            subject="Abstract Rejected – Conf2025",
            message=(
                f"Dear {obj.user.first_name},\n\n"
                f"Your abstract titled \"{obj.title}\" has unfortunately been REJECTED.\n"
                "For queries, please contact the conference organizers.\n\n"
                "Regards,\nConf2025 Secretariat"
            ),
            from_email=None,
            recipient_list=[obj.user.email],
            fail_silently=False,
        )
