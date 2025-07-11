from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html
from django.contrib import messages

from import_export.admin import ExportMixin

from .models import UserProfile, AbstractSubmission, CoAuthor
from .resources import AbstractSubmissionResource
from .forms import FullPaperUploadForm


# ------------------ User + UserProfile Inline ------------------

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Additional Info'

class CustomUserAdmin(BaseUserAdmin):  # not ModelAdmin!
    inlines = (UserProfileInline,)

# Unregister the default User admin and register the new one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ------------------ Abstract Submission Admin ------------------

class CoAuthorInline(admin.TabularInline):
    model = CoAuthor
    extra = 0
    readonly_fields = ('first_name', 'last_name', 'email', 'affiliation', 'designation')


class FullPaperUploadForm(forms.ModelForm):
    class Meta:
        model = AbstractSubmission
        fields = ['full_paper']


@admin.register(AbstractSubmission)
class AbstractSubmissionAdmin(ExportMixin, admin.ModelAdmin):
    form = FullPaperUploadForm
    resource_class = AbstractSubmissionResource

    list_display = (
        'paper_id', 'title',
        'corresponding_author_name', 'corresponding_author_email', 'main_author_phone',
        'corresponding_author_affiliation', 'corresponding_author_designation',
        'status', 'submitted_on', 'abstract_file_link', 'actions_column'
    )
    ordering = ('paper_id',)
    list_filter = ('status', 'institute', 'designation')
    search_fields = ('paper_id', 'name', 'user__email', 'keywords')
    readonly_fields = ('paper_id', 'submitted_on', 'abstract_file_link')
    list_editable = ('status',)
    inlines = [CoAuthorInline]
    actions = ['approve_selected', 'reject_selected']

    # Display fields
    def corresponding_author_name(self, obj):
        return obj.name
    corresponding_author_name.short_description = "Main Author"

    def main_author_phone(self, obj):
        return obj.user.userprofile.phone if hasattr(obj.user, 'userprofile') else "-"
    main_author_phone.short_description = "Phone"

    def corresponding_author_email(self, obj):
        return obj.user.email if obj.user and obj.user.email else "-"
    corresponding_author_email.short_description = "Email"

    def corresponding_author_affiliation(self, obj):
        return obj.institute or "-"
    corresponding_author_affiliation.short_description = "Affiliation"

    def corresponding_author_designation(self, obj):
        return obj.designation or "-"
    corresponding_author_designation.short_description = "Designation"

    def abstract_file_link(self, obj):
        if obj.abstract_file:
            return format_html('<a href="{}" target="_blank">View</a>', obj.abstract_file.url)
        return "No File"
    abstract_file_link.short_description = "Abstract File"

    # Actions column
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:pk>/', self.admin_site.admin_view(self.approve_abstract), name='abstract-approve'),
            path('reject/<int:pk>/', self.admin_site.admin_view(self.reject_abstract), name='abstract-reject'),
        ]
        return custom_urls + urls

    # Approve / Reject actions
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

    # Email notifications
    def send_approval_email(self, obj):
        send_mail(
            subject="Abstract Approved – IBSSC 2025",
            message=(
                f"Dear {obj.user.username},\n\n"
                f"It gives us immense pleasure to inform you that the Research Paper Scrutiny Committee has accepted "
                f"the abstract of your research paper with ID {obj.paper_id}, entitled “{obj.title}”, to be presented in the "
                f"“Indo Bhutan Social Science Conference” organised by the Department of Business Administration, Assam University, "
                f"to be held at Royal Thimphu College, Bhutan, from 3rd September 2025 to 6th September 2025.\n\n"
                f"You are further requested to submit the full-length paper and complete the registration process on or before "
                f"10th August 2025.\n\n"
                f"Note: If there are multiple authors in the paper, each author must register individually to receive a certificate.\n\n"
                f"👉 Join our official WhatsApp group to receive important conference updates:\n"
                f"https://chat.whatsapp.com/CPEaa6ek2ur0q6vL7nHJGT\n\n"
                f"Regards,\n"
                f"IBSSC Secretariat"
            ),
            from_email=None,  # Uses settings.DEFAULT_FROM_EMAIL
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
