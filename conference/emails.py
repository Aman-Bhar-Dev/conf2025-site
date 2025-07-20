from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_visitor_approval_email(visitor, amount=None):
    if amount is None:
        total_visitors = 1 + visitor.additional_visitors.count()
        amount = 15000 * total_visitors

    # Collect list of names (main + additional visitors)
    visitor_list = [visitor.name] + list(visitor.additional_visitors.values_list('name', flat=True))

    subject = "Your Visitor Registration for IBSSC 2025 Has Been Approved – Payment Required"
    context = {
        'visitor': visitor,
        'amount': amount,
        'visitor_list': visitor_list,
        'bank_details': {
            'account_name': "DBA CONFERENCE",
            'account_number': "0293102000006354",
            'bank_name': "IDBI BANK",
            'branch_name': "SILCHAR BRANCH",
            'swift_code': "IBKLINBB136",
            'ifsc_code': "IBKL0000293",
            'upi_id': "dbaconferenceassamuniversity@idbi"
        },
    }

    message = render_to_string('conference/visitors_payment.html', context)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [visitor.email],
        html_message=message,
        fail_silently=False,
    )

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_visitor_submission_confirmation(visitor):
    subject = "IBSSC 2025 – Visitor Application Received"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = visitor.email

    context = {
        "name": visitor.name,
        "email": visitor.email
    }

    html_content = render_to_string("conference/visitor_confirmation_email.html", context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
