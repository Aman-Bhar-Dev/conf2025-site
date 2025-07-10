from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary_storage.storage import MediaCloudinaryStorage

# -------------------------------
# USER PROFILE (for phone & institute)
# -------------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    institute = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# -------------------------------
# AbstractSubmission & CoAuthor
# -------------------------------
class AbstractSubmission(models.Model):
    main_author = models.CharField(max_length=255)
    email = models.EmailField()
    abstract_file = models.FileField(upload_to='abstracts/', storage=MediaCloudinaryStorage())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    paper_id = models.CharField(max_length=15, unique=True, editable=False, blank=True)
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    INSTITUTE_CHOICES = [
        ('Assam University, Silchar', 'Assam University, Silchar'),
        ('Royal Thimphu College, Bhutan', 'Royal Thimphu College, Bhutan'),
        ('Others', 'Others'),
    ]
    institute = models.CharField(max_length=100, choices=INSTITUTE_CHOICES)
    custom_institute = models.CharField(max_length=255, blank=True, null=True)

    DESIGNATION_CHOICES = [
        ('Student', 'Student'),
        ('Research Scholar', 'Research Scholar'),
        ('Professor', 'Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Corporate', 'Corporate'),
    ]
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)

    keywords = models.TextField()
    full_paper = models.FileField(
    upload_to='full_papers/',
    blank=True,
    null=True,
    storage=MediaCloudinaryStorage()
)



    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    submitted_on = models.DateTimeField(auto_now_add=True)

    MODE_CHOICES = [('Online', 'Online'), ('Offline', 'Offline')]
    CATEGORY_CHOICES = [
        ('Academician', 'Academician'),
        ('Corporate', 'Corporate'),
        ('Student', 'Research Scholar / Student'),
        ('NonPresenter', 'Non-presenter / Listener'),
        ('International', 'International (Non-Indian, Non-Bhutanese)')
    ]

    mode_of_participation = models.CharField(max_length=10, choices=MODE_CHOICES, default='Offline')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Student', blank=True)
    payment_amount = models.IntegerField(default=0)
    payment_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.paper_id:
            last = AbstractSubmission.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.paper_id = f"IBSSC{10000 + next_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.paper_id} - {self.title}"

    def _get_full_name(self, index):
        coauthors = list(self.coauthors.all())
        if len(coauthors) > index:
            return f"{coauthors[index].first_name} {coauthors[index].last_name}"
        return ''

    def _get_coauthor_attr(self, index, attr):
        coauthors = list(self.coauthors.all())
        if len(coauthors) > index:
            return getattr(coauthors[index], attr, '')
        return ''

    def get_coauthor1_name(self): return self._get_full_name(0)
    def get_coauthor1_email(self): return self._get_coauthor_attr(0, 'email')
    def get_coauthor1_designation(self): return self._get_coauthor_attr(0, 'designation')
    def get_coauthor2_name(self): return self._get_full_name(1)
    def get_coauthor2_email(self): return self._get_coauthor_attr(1, 'email')
    def get_coauthor2_designation(self): return self._get_coauthor_attr(1, 'designation')
    def get_coauthor3_name(self): return self._get_full_name(2)
    def get_coauthor3_email(self): return self._get_coauthor_attr(2, 'email')
    def get_coauthor3_designation(self): return self._get_coauthor_attr(2, 'designation')
    def get_coauthor4_name(self): return self._get_full_name(3)
    def get_coauthor4_email(self): return self._get_coauthor_attr(3, 'email')
    def get_coauthor4_designation(self): return self._get_coauthor_attr(3, 'designation')
    def get_coauthor5_name(self): return self._get_full_name(4)
    def get_coauthor5_email(self): return self._get_coauthor_attr(4, 'email')
    def get_coauthor5_designation(self): return self._get_coauthor_attr(4, 'designation')
    def get_coauthor1_affiliation(self): return self._get_coauthor_attr(0, 'affiliation')
    def get_coauthor2_affiliation(self): return self._get_coauthor_attr(1, 'affiliation')
    def get_coauthor3_affiliation(self): return self._get_coauthor_attr(2, 'affiliation')
    def get_coauthor4_affiliation(self): return self._get_coauthor_attr(3, 'affiliation')
    def get_coauthor5_affiliation(self): return self._get_coauthor_attr(4, 'affiliation')

    class Meta:
        verbose_name = "Abstract Submission"
        verbose_name_plural = "Abstract Submissions"
        ordering = ['paper_id']


class CoAuthor(models.Model):
    submission = models.ForeignKey(AbstractSubmission, on_delete=models.CASCADE, related_name='coauthors')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    affiliation = models.CharField(max_length=200)
    designation = models.CharField(
        max_length=100,
        choices=[
            ('Student', 'Student'),
            ('Research Scholar', 'Research Scholar'),
            ('Assistant Professor', 'Assistant Professor'),
            ('Associate Professor', 'Associate Professor'),
            ('Professor', 'Professor'),
            ('Corporate', 'Corporate'),
        ]
    )
    category = models.CharField(
        max_length=30,
        choices=[
            ('Academician', 'Academician'),
            ('Corporate', 'Corporate'),
            ('Student', 'Research Scholar / Student'),
            ('NonPresenter', 'Non-presenter / Listener'),
            ('International', 'International (Non-Indian, Non-Bhutanese)'),
        ],
        default='Student'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class ParticipationInfo(models.Model):
    submission = models.OneToOneField(AbstractSubmission, on_delete=models.CASCADE)
    author_participation_mode = models.CharField(max_length=10, choices=[('Online', 'Online'), ('Offline', 'Offline')])
    author_identity_proof = models.FileField(
    upload_to='identity_proofs/',
    blank=True,
    null=True,
    storage=MediaCloudinaryStorage()
)

    total_amount = models.IntegerField(default=0)
    confirmed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ParticipationInfo for {self.submission.paper_id}"


class CoAuthorParticipation(models.Model):
    participation_info = models.ForeignKey(ParticipationInfo, on_delete=models.CASCADE, related_name='coauthor_details')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    participation_mode = models.CharField(
        max_length=10,
        choices=[
            ('None', 'Not Attending'),
            ('Online', 'Online'),
            ('Offline', 'Offline')
        ],
        default='None'
    )
    identity_proof = models.FileField(
    upload_to='identity_proofs/',
    blank=True,
    null=True,
    storage=MediaCloudinaryStorage()
)


    def __str__(self):
        return f"{self.name} ({self.participation_mode})"


class FinalRegistration(models.Model):
    submission = models.OneToOneField(AbstractSubmission, on_delete=models.CASCADE)
    author_mode = models.CharField(max_length=10, choices=[('Online', 'Online'), ('Offline', 'Offline')])
    author_identity_proof = models.FileField(upload_to='identity_proofs/')
    total_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class FinalParticipant(models.Model):
    registration = models.ForeignKey(FinalRegistration, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    affiliation = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=[('CoAuthor', 'Co-Author'), ('Visitor', 'Visitor')])
    mode = models.CharField(max_length=10, choices=[('Online', 'Online'), ('Offline', 'Offline')])
    identity_proof = models.FileField(
    upload_to='identity_proofs/',
    blank=True,
    null=True,
    storage=MediaCloudinaryStorage()
)

