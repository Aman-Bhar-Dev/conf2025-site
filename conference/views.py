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


from .models import (
    AbstractSubmission, CoAuthor,
    FinalRegistration, FinalParticipant,
    ParticipationInfo, CoAuthorParticipation
)

from .forms import (
    AbstractSubmissionForm,
    FullPaperUploadForm,
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

            if submission.institute == "Others":
                custom = form.cleaned_data.get("custom_institute")
                if custom:
                    submission.institute = custom.strip()
            uploaded_file = request.FILES.get('abstract_file')
            if uploaded_file:
                result = cloudinary.uploader.upload(
                    uploaded_file,
                    resource_type='raw',
                    folder='abstracts/',
                    public_id=os.path.splitext(uploaded_file.name)[0]
                )
                submission.abstract_file.name = result['public_id']

            submission.save()

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

You can now proceed to payment if not already done.
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


# ============ PARTICIPATION & PAYMENT ============ #
@login_required
def confirm_participation_view(request, paper_id):
    submission = get_object_or_404(AbstractSubmission, paper_id=paper_id, user=request.user)
    coauthors = CoAuthor.objects.filter(submission=submission)

    if request.method == 'POST':
        author_mode = request.POST.get('author_mode')
        author_proof = request.FILES.get('author_identity_proof')

        pinfo = ParticipationInfo.objects.create(
            submission=submission,
            author_participation_mode=author_mode,
            author_identity_proof=author_proof,
        )

        total = calculate_fee(submission.category, author_mode, submission.institute)

        for idx, co in enumerate(coauthors):
            mode = request.POST.get(f'coauthor_mode_{idx}')
            proof = request.FILES.get(f'coauthor_proof_{idx}')
            CoAuthorParticipation.objects.create(
                participation_info=pinfo,
                name=f"{co.first_name} {co.last_name}",
                email=co.email,
                participation_mode=mode,
                identity_proof=proof,
            )
            total += calculate_fee(co.category, mode, co.affiliation)

        pinfo.total_amount = total
        pinfo.save()
        return redirect('payment', paper_id=submission.paper_id)

    return render(request, 'conference/confirm_participation.html', {
        'submission': submission,
        'coauthors': coauthors,
    })


@login_required
def checkout_view(request, paper_id):
    submission = get_object_or_404(AbstractSubmission, paper_id=paper_id, user=request.user)

    if submission.payment_status:
        messages.error(request, "You have already completed payment.")
        return redirect('payment', paper_id=paper_id)

    try:
        registration = FinalRegistration.objects.get(submission=submission)
        participants = registration.participants.all()
    except FinalRegistration.DoesNotExist:
        registration = None
        participants = []

    coauthors = submission.coauthors.all()

    if request.method == 'POST':
        if registration:
            registration.participants.all().delete()
            registration.delete()

        author_mode = request.POST.get('author_mode')
        author_proof = request.FILES.get('author_identity_proof')
        total = calculate_fee(submission.category, author_mode, submission.institute)

        registration = FinalRegistration.objects.create(
            submission=submission,
            author_mode=author_mode,
            author_identity_proof=author_proof,
            total_amount=0
        )

        for idx, co in enumerate(coauthors):
            mode = request.POST.get(f'coauthor_mode_{idx}')
            proof = request.FILES.get(f'coauthor_proof_{idx}')
            if mode != 'None':
                FinalParticipant.objects.create(
                    registration=registration,
                    name=f"{co.first_name} {co.last_name}",
                    email=co.email,
                    affiliation=co.affiliation,
                    role='CoAuthor',
                    mode=mode,
                    identity_proof=proof
                )
                total += calculate_fee(co.category, mode, co.affiliation)

        visitor_count = int(request.POST.get('visitor_count', 0))
        for i in range(visitor_count):
            name = request.POST.get(f'visitor_name_{i}')
            email = request.POST.get(f'visitor_email_{i}')
            affiliation = request.POST.get(f'visitor_affiliation_{i}')
            mode = request.POST.get(f'visitor_mode_{i}')
            proof = request.FILES.get(f'visitor_proof_{i}')
            if name and email and affiliation and mode:
                FinalParticipant.objects.create(
                    registration=registration,
                    name=name,
                    email=email,
                    affiliation=affiliation,
                    role='Visitor',
                    mode=mode,
                    identity_proof=proof
                )
                total += calculate_fee('NonPresenter', mode, affiliation)

        registration.total_amount = total
        registration.save()
        return redirect('payment_summary', paper_id=paper_id)

    return render(request, 'conference/checkout.html', {
        'submission': submission,
        'coauthors': coauthors,
        'registration': registration,
        'participants': participants,
    })


@login_required
def payment_view(request, paper_id):
    submission = get_object_or_404(AbstractSubmission, paper_id=paper_id, user=request.user)

    try:
        registration = FinalRegistration.objects.get(submission=submission)
    except FinalRegistration.DoesNotExist:
        messages.error(request, "Please complete final registration before proceeding to payment.")
        return redirect('checkout', paper_id=paper_id)

    if submission.status != 'APPROVED':
        messages.error(request, "You can only pay after your abstract is approved.")
        return redirect('profile')

    return render(request, 'conference/payment.html', {
        'submission': submission,
        'registration': registration,
        'participants': registration.participants.all(),
        'amount': registration.total_amount
    })


@login_required
def payment_summary(request, paper_id):
    submission = get_object_or_404(AbstractSubmission, paper_id=paper_id, user=request.user)
    try:
        registration = FinalRegistration.objects.get(submission=submission)
        participants = FinalParticipant.objects.filter(registration=registration)
    except FinalRegistration.DoesNotExist:
        messages.error(request, "Final registration not found.")
        return redirect('checkout', paper_id=paper_id)

    return render(request, 'conference/payment.html', {
        'submission': submission,
        'registration': registration,
        'participants': participants,
        'amount': registration.total_amount,
        'payment_pending': True
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


# ============ UTILITY ============ #
def calculate_fee(category, mode, institute):
    if mode == 'Offline':
        if category == 'Corporate':
            amount = 20000
        elif category in ['Academician', 'Student']:
            amount = 16000
        elif category == 'NonPresenter':
            amount = 15000
        elif category == 'International':
            amount = 20000
        else:
            amount = 16000

        if 'assam university' in institute.lower():
            amount -= 1000
    elif mode == 'Online':
        amount = 2000 if category == 'Corporate' else 1000
    else:
        amount = 0
    return amount

def pricing_view(request):
    return render(request, 'conference/pricing.html')
