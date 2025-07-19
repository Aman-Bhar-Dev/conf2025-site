from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden
import re
import cloudinary
import cloudinary.uploader
import os


from .models import (
    AbstractSubmission, CoAuthor,
    FinalRegistration, FinalParticipant,
)


# ============ HOME ============ #
def index(request):
    return render(request, 'conference/index.html')


# ============ AUTHENTICATION ============ #
def signup_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        institution = request.POST.get('institution')
        if institution == 'Others':
            institution = request.POST.get('custom_institution') or institution

        password = request.POST.get('password')
        confirm = request.POST.get('confirm-password')

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('signup')

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d).{8,}$', password):
            messages.error(request, "Password must be at least 8 characters long and include both letters and numbers.")
            return redirect('signup')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name
        )

        user.profile.phone = phone
        user.profile.institution = institution.strip()
        user.profile.save()

        login(request, user)
        return redirect('home')

    return render(request, 'conference/signup.html')


def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or '/'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('home')
        messages.error(request, "Invalid email or password.")
    return render(request, 'conference/login.html', {'next': next_url})


def logout_view(request):
    logout(request)
    return redirect('home')


# ============ ABSTRACT SUBMISSION ============ #
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
import cloudinary.uploader
import os

from .forms import AbstractSubmissionForm
from .models import AbstractSubmission, CoAuthor


@login_required
def abstract_submit(request):
    if request.method == 'POST':
        form = AbstractSubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.mode_of_participation = request.POST.get('mode_of_participation')
            submission.category = request.POST.get('category')
            submission.email = request.user.email
            submission.main_author = request.user.get_full_name() or request.user.username

            # Custom institute logic
            if submission.institute == "Others":
                custom = form.cleaned_data.get("custom_institute")
                if custom:
                    submission.institute = custom.strip()

            # Use built-in Django file saving (Cloudinary will handle it)
            uploaded_file = request.FILES.get('abstract_file')
            if uploaded_file and uploaded_file.size > 0:
                submission.abstract_file = uploaded_file
            else:
                messages.error(request, "Uploaded file is empty.")
                return render(request, 'conference/abstract_submit.html', {'form': form})

            submission.save()

            # Save co-authors
            for i in range(20):
                first = request.POST.get(f'coauthor_first_name_{i}')
                last = request.POST.get(f'coauthor_last_name_{i}')
                email = request.POST.get(f'coauthor_email_{i}')
                affil = request.POST.get(f'coauthor_institute_{i}')
                custom_affil = request.POST.get(f'coauthor_custom_institute_{i}')
                designation = request.POST.get(f'coauthor_designation_{i}')
                category = request.POST.get(f'coauthor_category_{i}')

                if first and last and email:
                    affiliation_final = custom_affil.strip() if affil == 'Others' and custom_affil else affil
                    CoAuthor.objects.create(
                        submission=submission,
                        first_name=first.strip(),
                        last_name=last.strip(),
                        email=email.strip(),
                        affiliation=affiliation_final,
                        designation=designation or '',
                        category=category or 'Student'
                    )

            # Confirmation email
            send_mail(
                subject="IBSSC 2025 - Abstract Submission Confirmation",
                message=f"""Dear {request.user.first_name},

Thank you for submitting your abstract to IBSSC 2025. Our team will review your submission and notify you of the next steps.

Regards,  
IBSSC2025 Secretariat
""",
                from_email=None,
                recipient_list=[request.user.email],
            )

            messages.success(request, "Abstract submitted successfully.")
            return redirect('thankyouab')

        else:
            messages.error(request, "There was an error with your submission.")

    else:
        form = AbstractSubmissionForm()

    return render(request, 'conference/abstract_submit.html', {'form': form})



def thank_you_abstract(request):
    return render(request, 'conference/thankyouab.html')


# ============ PROFILE & FULL PAPER ============ #
@login_required
def profile_view(request):
    submissions = AbstractSubmission.objects.filter(user=request.user)

    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        submission = get_object_or_404(AbstractSubmission, id=submission_id, user=request.user)
        form = FullPaperUploadForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            send_mail(
                subject="Final Paper Uploaded Successfully – Conf2025",
                message=f'''Dear {request.user.first_name},

Your final paper for the abstract titled "{submission.title}" has been successfully uploaded.

View your profile here: https://ibsscconf-site.onrender.com/profile/

Regards,  
IBSSC2025 Secretariat
''',
                from_email=None,
                recipient_list=[request.user.email]
            )
            messages.success(request, "Full paper uploaded successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Invalid full paper upload.")
    else:
        form = FullPaperUploadForm()

    return render(request, 'conference/profile.html', {
        'submissions': submissions,
        'upload_form': form
    })

# ============ STATIC PAGES ============ #
def thank_you(request):
    return render(request, 'conference/thankyou.html')

def about(request):
    return render(request, 'conference/about.html')

def contact(request):
    return render(request, 'conference/contact.html')

def itinerary(request):
    return render(request, 'conference/itinerary.html')

def pricing_view(request):
    return render(request, 'conference/pricing.html')

# ---------- Payment realted work here ----------#

from .models import FinalRegistration, FinalParticipant  # Make sure these are imported
# [...] (keep all your previous imports and unchanged code)

def calculate_fee(category, mode, institute):
    if not mode or mode == 'None':
        return 0

    if category == 'NonPresenter':
        return 15000

    if category == 'International':
        return 20750 if mode == 'Offline' else 8300

    if mode == 'Offline':
        if category == 'Corporate':
            amount = 20000
        elif category in ['Academician', 'Student']:
            amount = 16000
        else:
            amount = 16000
    elif mode == 'Online':
        if category == 'Corporate':
            amount = 2000
        else:
            amount = 1000
    else:
        amount = 0

    if mode == 'Offline' and institute and 'assam university' in institute.lower():
        amount -= 1000

    return amount


@login_required
def checkout_view(request, paper_id):
    submission = get_object_or_404(AbstractSubmission, paper_id=paper_id, user=request.user)
    coauthors = CoAuthor.objects.filter(submission=submission)

    if request.method == 'POST':
        FinalRegistration.objects.filter(submission=submission).delete()

        author_mode = request.POST.get('author_mode')
        author_proof = request.FILES.get('author_identity_proof')
        author_phone = request.POST.get('author_phone')
        author_address = request.POST.get('author_address')
        author_gender = request.POST.get('author_gender')
        presenter = request.POST.get('presenter')
        selected_theme = request.POST.get('selected_theme')


        if author_mode == "Offline" and not author_proof:
            messages.error(request, "Main author selected Offline but did not upload identity proof.")
            return redirect('checkout', paper_id=paper_id)

        total = calculate_fee(submission.category, author_mode, submission.institute)

        registration = FinalRegistration.objects.create(
            submission=submission,
            author_name=submission.main_author,
            author_designation=submission.designation,
            author_mode=author_mode,
            author_contact=author_phone,
            author_address=author_address,
            author_gender=author_gender,
            author_id_proof=author_proof,
            presenter_name=presenter,
            selected_theme=selected_theme,
            total_amount=0
        )

        # Co-authors
        for idx, co in enumerate(coauthors):
            mode = request.POST.get(f'coauthor_mode_{idx}')
            proof = request.FILES.get(f'coauthor_proof_{idx}')
            phone = request.POST.get(f'coauthor_phone_{idx}')
            address = request.POST.get(f'coauthor_address_{idx}')
            gender = request.POST.get(f'coauthor_gender_{idx}')

            if not mode:
                messages.error(request, f"Mode not selected for co-author {co.first_name} {co.last_name}.")
                return redirect('checkout', paper_id=paper_id)

            if mode == 'Offline' and not proof:
                messages.error(request, f"Co-author {co.first_name} selected Offline but did not upload identity proof.")
                return redirect('checkout', paper_id=paper_id)

            institute = co.affiliation or ''
            fee = calculate_fee(co.category, mode, institute)
            total += fee

            FinalParticipant.objects.create(
                registration=registration,
                name=f"{co.first_name} {co.last_name}",
                email=co.email,
                contact=phone,
                gender=gender,
                address=address,
                role="CoAuthor",
                mode=mode,
                id_proof=proof,
                affiliation=co.affiliation
            )

        # Visitors
        visitor_count = 0
        while request.POST.get(f'visitor_name_{visitor_count}'):
            name = request.POST.get(f'visitor_name_{visitor_count}')
            email = request.POST.get(f'visitor_email_{visitor_count}')
            mode = request.POST.get(f'visitor_mode_{visitor_count}')
            proof = request.FILES.get(f'visitor_proof_{visitor_count}')
            phone = request.POST.get(f'visitor_phone_{visitor_count}')
            address = request.POST.get(f'visitor_address_{visitor_count}')
            gender = request.POST.get(f'visitor_gender_{visitor_count}')

            if mode == 'Offline' and not proof:
                messages.error(request, f"Visitor '{name}' selected Offline but did not upload identity proof.")
                return redirect('checkout', paper_id=paper_id)

            total += 15000  # Fixed visitor fee

            FinalParticipant.objects.create(
                registration=registration,
                name=name,
                email=email,
                contact=phone,
                gender=gender,
                address=address,
                role="Visitor",
                mode=mode,
                id_proof=proof
            )

            visitor_count += 1

        registration.total_amount = total
        registration.save()

        return redirect('payment_summary', paper_id=submission.paper_id)

    return render(request, 'conference/checkout.html', {
        'submission': submission,
        'coauthors': coauthors
    })

#qr code related work here#

from django.shortcuts import render
import qrcode
import io
import base64
from .forms import PaymentConfirmationForm
@login_required
def payment_summary_view(request, paper_id):
    submission = get_object_or_404(AbstractSubmission, paper_id=paper_id, user=request.user)
    registration = get_object_or_404(FinalRegistration, submission=submission)
    participants = FinalParticipant.objects.filter(registration=registration)

    # Payment breakdown
    breakdown = []

    # Main author
    author_fee = calculate_fee(
        submission.category,
        registration.author_mode,
        submission.institute
    )
    breakdown.append({
        "name": registration.author_name,
        "role": "Main Author",
        "mode": registration.author_mode,
        "fee": author_fee
    })

    # Co-authors and visitors
    for p in participants:
        if p.role == "CoAuthor":
            category = next((co.category for co in CoAuthor.objects.filter(submission=submission, email=p.email)), "Student")
            fee = calculate_fee(category, p.mode, (p.affiliation or "").lower())

        elif p.role == "Visitor":
            fee = 15000
        else:
            fee = 0
        breakdown.append({
            "name": p.name,
            "role": p.role,
            "mode": p.mode,
            "fee": fee
        })

    # Generate QR Code
    upi_id = "dbaconferenceassamuniversity@idbi"
    name = "IBSSC 2025"
    amount = registration.total_amount
    upi_link = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"

    qr = qrcode.make(upi_link)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    if request.method == 'POST':
        form = PaymentConfirmationForm(request.POST, request.FILES, instance=registration)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment information submitted successfully.")
            return redirect('thank_you')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PaymentConfirmationForm(instance=registration)

    return render(request, 'conference/payment_summary.html', {
        'submission': submission,
        'registration': registration,
        'breakdown': breakdown,
        'qr_code': img_str,
        'upi_id': upi_id,
        'amount': amount,
        'form': form,
    })


@login_required
def thank_you_view(request):
    submission = AbstractSubmission.objects.filter(user=request.user).latest('submitted_on')
    final_reg = get_object_or_404(FinalRegistration, submission=submission)

    return render(request, 'conference/confirmation.html', {
        "submission": submission,
        "final_reg": final_reg,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import FinalRegistration, FinalParticipant

@login_required
def payment_confirmation_view(request):
    # Grab the most recent FinalRegistration for this user:
    final_reg = (
        FinalRegistration.objects
        .filter(submission__user=request.user)
        .order_by('-created_at')
        .first()
    )
    if not final_reg:
        # no registration found—redirect or show an error
        return redirect('profile')

    # Pull out submission and participants
    submission = final_reg.submission
    coauthors   = final_reg.participants.filter(role='CoAuthor')
    visitors    = final_reg.participants.filter(role='Visitor')

    return render(request, "conference/confirmation.html", {
        "submission": submission,
        "final_reg": final_reg,
        "coauthors": coauthors,
        "visitors": visitors,
    })
#email for payment confirmation#
from .models import FinalRegistration, FinalParticipant, CoAuthor, AbstractSubmission
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_payment_receipt_email(registration):
    # Main author affiliation
    main_inst = registration.submission.institute

    # Gather co‑authors
    coauthor_objs = registration.participants.filter(role='CoAuthor')
    coauthors = [
        {
            'name': p.name,
            'affiliation': p.affiliation or 'N/A',
        }
        for p in coauthor_objs
    ]

    # Gather visitors
    visitor_objs = registration.participants.filter(role='Visitor')
    visitors = [
        {
            'name': p.name,
            'contact': p.contact,
        }
        for p in visitor_objs
    ]

    # Payment breakdown
    breakdown = []
    # main author
    breakdown.append({
        'role': 'Main Author',
        'name': registration.author_name,
        'fee': registration.total_amount if not coauthor_objs and not visitor_objs else None,  
        # We'll fill in exact fees next
    })
    # Actually compute each fee
    total = 0
    # reuse your calculate_fee logic
    from .views import calculate_fee
    fee_main = calculate_fee(
        registration.submission.category,
        registration.author_mode,
        registration.submission.institute
    )
    breakdown = [{
        'role': 'Main Author',
        'name': registration.author_name,
        'fee': fee_main,
    }]
    total += fee_main

    for p in coauthor_objs:
        # find category from CoAuthor model
        cat = CoAuthor.objects.get(
            submission=registration.submission, email=p.email
        ).category
        fee = calculate_fee(cat, p.mode, (p.affiliation or '').lower())
        breakdown.append({
            'role': 'Co-Author',
            'name': p.name,
            'fee': fee,
        })
        total += fee

    for p in visitor_objs:
        fee = 15000
        breakdown.append({
            'role': 'Visitor',
            'name': p.name,
            'fee': fee,
        })
        total += fee

    subject = "Payment Confirmed – IBSSC 2025"
    to_email = registration.submission.user.email
    context = {
        'name': registration.author_name,
        'affiliation': main_inst,
        'paper_id': registration.submission.paper_id,
        'paper_title': registration.submission.title,
        'theme': registration.selected_theme,
        'total_amount': total,
        'transaction_id': registration.transaction_id,
        'transaction_date': registration.transaction_date,
        'coauthors': coauthors,
        'visitors': visitors,
        'breakdown': breakdown,
    }

    html_content = render_to_string('payment_receipt.html', context)
    email = EmailMessage(subject, html_content, to=[to_email])
    email.content_subtype = "html"
    email.send()
