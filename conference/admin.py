from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html
from django.contrib import messages
from .resources import FinalRegistrationResource
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

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import CoAuthor
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
        user = obj.user
        coauthors = CoAuthor.objects.filter(submission=obj)

        context = {
            'author_name': user.get_full_name() or user.username,
            'title': obj.title,
            'paper_id': obj.paper_id,
            'affiliation': obj.institute,
            'coauthors': coauthors
        }

        html_content = render_to_string('conference/abstract_approved.html', context)

        email = EmailMessage(
            subject="Abstract Approved – IBSSC 2025",
            body=html_content,
            to=[user.email]
        )
        email.content_subtype = "html"
        email.send()

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



from django.contrib import admin
from import_export.admin import ExportMixin
from django.utils.html import format_html
from .models import FinalRegistration, FinalParticipant
from .resources import FinalRegistrationResource


class FinalParticipantInline(admin.TabularInline):
    model = FinalParticipant
    extra = 0
    readonly_fields = (
        'name', 'email', 'contact', 'gender', 'address',
        'role', 'mode', 'affiliation'
    )
    can_delete = False
    show_change_link = False


# ---------- FinalRegistration Admin Setup ----------

# conference/admin.py

from django.contrib import admin
from import_export.admin import ExportMixin
from django.utils.html import format_html

from .models import FinalRegistration, FinalParticipant
from .resources import FinalRegistrationResource
from .views import send_payment_receipt_email  # your email‑sender

class FinalParticipantInline(admin.TabularInline):
    model = FinalParticipant
    readonly_fields = (
        'name','email','contact','gender','address','role','mode','affiliation'
    )
    extra = 0
    can_delete = False
    show_change_link = False

@admin.action(description="✅ Mark as payment verified & send receipt email")
def mark_payment_verified(modeladmin, request, queryset):
    sent = 0
    for reg in queryset:
        if not reg.payment_verified:
            reg.payment_verified = True
            reg.save()
            send_payment_receipt_email(reg)
            sent += 1
    modeladmin.message_user(request, f"{sent} receipt email(s) sent.")

@admin.register(FinalRegistration)
class FinalRegistrationAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = FinalRegistrationResource
    inlines       = [FinalParticipantInline]
    list_display  = (
        'submission','author_name','author_mode',
        'total_amount','payment_verified','screenshot_preview'
    )
    list_filter   = ('author_mode','payment_verified')
    search_fields = (
        'submission__paper_id','submission__title',
        'submission__user__email',
    )
    actions = [mark_payment_verified]

    def author_name(self, obj):
        return obj.submission.user.get_full_name()

    def screenshot_preview(self, obj):
        if obj.payment_screenshot:
            return format_html(
                '<a href="{0}" target="_blank">'
                '<img src="{0}" style="max-height:100px;"/></a>',
                obj.payment_screenshot.url
            )
        return 'No screenshot'
    screenshot_preview.short_description = 'Screenshot'

    def save_model(self, request, obj, form, change):
        """
        When saving from the detail page, if payment_verified was just checked,
        send the receipt email.
        """
        # Only on edits, and only if the field actually changed to True
        if change and 'payment_verified' in form.changed_data and obj.payment_verified:
            send_payment_receipt_email(obj)

        super().save_model(request, obj, form, change)

# conference/admin.py

from django.contrib import admin
from .models import VisitorRegistration



# conference/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import VisitorRegistration, AdditionalVisitor
from .emails import send_visitor_approval_email

class AdditionalVisitorInline(admin.TabularInline):
    model = AdditionalVisitor
    extra = 0

@admin.register(VisitorRegistration)
class VisitorRegistrationAdmin(ExportMixin,admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'timestamp')
    list_filter  = ('status', 'timestamp')
    inlines      = [AdditionalVisitorInline]

    actions = ['approve_and_send_email']

    @admin.action(description=_("Approve selected registrations and send payment email"))
    def approve_and_send_email(self, request, queryset):
        for registration in queryset:
            if registration.status != 'Approved':
                # 1. Mark approved
                registration.status = 'Approved'
                registration.save()

                # 2. Calculate total fee: ₹15,000 per visitor
                num_additional = registration.additional_visitors.count()
                total_visitors = 1 + num_additional
                amount = total_visitors * 15000  # in INR

                # 3. Send email with the computed amount
                print(f"[DEBUG] Name: {registration.name}, Additional Count: {num_additional}, Total Amount: ₹{amount}")

                send_visitor_approval_email(registration, amount)

        self.message_user(request, _("Selected registrations approved and emails sent."))
@admin.action(description="✅ Approve selected visitor applications")
def approve_visitors(modeladmin, request, queryset):
    updated = queryset.update(status='Approved')
    modeladmin.message_user(request, f"{updated} application(s) approved.")

@admin.action(description="❌ Reject selected visitor applications")
def reject_visitors(modeladmin, request, queryset):
    updated = queryset.update(status='Rejected')
    modeladmin.message_user(request, f"{updated} application(s) rejected.")

