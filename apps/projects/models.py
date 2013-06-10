from apps.wallposts.models import WallPost
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import truncate_words
from django.utils.translation import ugettext as _
from django.conf import settings
from django_extensions.db.fields import ModificationDateTimeField, CreationDateTimeField
from djchoices import DjangoChoices, ChoiceItem
from sorl.thumbnail import ImageField
from taggit_autocomplete_modified.managers import TaggableManagerAutocomplete as TaggableManager
from apps.bluebottle_utils.fields import MoneyField
from apps.fund.models import Donation
from django.template.defaultfilters import slugify


class ProjectTheme(models.Model):
    """ Themes for Projects. """

    # The name is marked as unique so that users can't create duplicate theme names.
    name = models.CharField(_("name"), max_length=100, unique=True)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _("project theme")
        verbose_name_plural = _("project themes")


class ProjectPhases(DjangoChoices):
    pitch = ChoiceItem('pitch', label=_("Pitch"))
    plan = ChoiceItem('plan', label=_("Plan"))
    campaign = ChoiceItem('campaign', label=_("Campaign"))
    results = ChoiceItem('results', label=_("Results"))


class Project(models.Model):
    """ The base Project model. """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("owner"), related_name="owner")

    team_member = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("project team member"), related_name="team_member", null=True, blank=True)

    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)

    phase = models.CharField(_("phase"), max_length=20, choices=ProjectPhases.choices, help_text=_("Phase this project is in right now."))

    created = CreationDateTimeField(_("created"), help_text=_("When this project was created."))

    organization = models.ForeignKey('organizations.Organization', verbose_name=_("organisation"), blank=True, null=True)

    # FIXME: Implement money_asked & money_donated
    @property
    def money_donated(self):
        return 100000

    @property
    def money_asked(self):
        return 400000

    def __unicode__(self):
        if self.title:
            return self.title
        return self.slug

    @property
    def supporters_count(self, with_guests=True):
        # TODO: Replace this with a proper Supporters API
        # something like /projects/<slug>/donations
        donations = Donation.objects.filter(project=self)
        donations = donations.filter(status__in=[Donation.DonationStatuses.paid, Donation.DonationStatuses.in_progress])
        donations = donations.filter(user__isnull=False)
        donations = donations.annotate(Count('user'))
        count = len(donations.all())

        if with_guests:
            donations = Donation.objects.filter(project=self)
            donations = donations.filter(status__in=[Donation.DonationStatuses.paid, Donation.DonationStatuses.in_progress])
            donations = donations.filter(user__isnull=True)
            count = count + len(donations.all())
        return count

    @models.permalink
    def get_absolute_url(self):
        """ Get the URL for the current project. """
        return 'project-detail', (), {'slug': self.slug}

    class Meta:
        ordering = ['title']
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.phase:
            self.phase = ProjectPhases.pitch
        super(Project, self).save(*args, **kwargs)


class ProjectNeedChoices(DjangoChoices):
    skills = ChoiceItem('skills', label=_("Skills and expertise"))
    finance = ChoiceItem('finance', label=_("Crowdfunding campaign"))
    both = ChoiceItem('both', label=_("Both"))


class ProjectPitch(models.Model):

    class PitchStatuses(DjangoChoices):
        new = ChoiceItem('new', label=_("New"))
        submitted = ChoiceItem('submitted', label=_("Submitted"))
        rejected = ChoiceItem('rejected', label=_("Rejected"))
        approved = ChoiceItem('approved', label=_("Approved"))

    project = models.OneToOneField("projects.Project", verbose_name=_("project"))
    status = models.CharField(_("status"), max_length=20, choices=PitchStatuses.choices)

    created = CreationDateTimeField(_("created"), help_text=_("When this project was created."))
    updated = ModificationDateTimeField(_('updated'))

    # Basics
    title = models.CharField(_("title"), max_length=100, help_text=_("Be short, creative, simple and memorable"))
    pitch = models.TextField(_("pitch"), blank=True, help_text=_("Pitch your smart idea in one sentence"))
    description = models.TextField(_("why, what and how"), help_text=_("Blow us away with the details!"), blank=True)

    need = models.CharField(_("Project need"), null=True, max_length=20, choices=ProjectNeedChoices.choices, default=ProjectNeedChoices.both)
    theme = models.ForeignKey(ProjectTheme, blank=True, null=True, verbose_name=_("theme"), help_text=_("Select one of the themes "))
    tags = TaggableManager(blank=True, verbose_name=_("tags"), help_text=_("Add tags"))

    # Location
    latitude = models.DecimalField(_("latitude"), max_digits=21, decimal_places=18, null=True, blank=True)
    longitude = models.DecimalField(_("longitude"), max_digits=21, decimal_places=18, null=True, blank=True)
    country = models.ForeignKey('geo.Country', blank=True, null=True)

    # Media
    image = ImageField(_("picture"), max_length=255, blank=True, upload_to='project_images/', help_text=_("Upload the picture that best describes your smart idea!"))
    video_url = models.URLField(_("video"), max_length=100, blank=True, default='', help_text=_("Do you have a video pitch or a short movie that explains your project. Cool! We can't wait to see it. You can paste the link to the YouTube or Vimeo video here"))


    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('pitch')
        verbose_name_plural = _('pitches')


class ProjectPlan(models.Model):

    class PlanStatuses(DjangoChoices):
        new = ChoiceItem('new', label=_("New"))
        submitted = ChoiceItem('submitted', label=_("Submitted"))
        rejected = ChoiceItem('rejected', label=_("Rejected"))
        needs_work = ChoiceItem('needs_work', label=_("Needs work"))
        approved = ChoiceItem('approved', label=_("Approved"))

    project = models.OneToOneField("projects.Project", verbose_name=_("project"))
    status = models.CharField(_("status"), max_length=20, choices=PlanStatuses.choices)

    created = CreationDateTimeField(_("created"), help_text=_("When this project was created."))
    updated = ModificationDateTimeField(_('updated'))

    # Basics
    title = models.CharField(_("title"), max_length=100, help_text=_("Be short, creative, simple and memorable"))
    pitch = models.TextField(_("pitch"), blank=True, help_text=_("Pitch your smart idea in one sentence"))

    need = models.CharField(_("Project need"), null=True, max_length=20, choices=ProjectNeedChoices.choices, default=ProjectNeedChoices.both)
    theme = models.ForeignKey(ProjectTheme, blank=True, null=True, verbose_name=_("theme"), help_text=_("Select one of the themes "))
    tags = TaggableManager(blank=True, verbose_name=_("tags"), help_text=_("Add tags"))

    # Extended Description
    description = models.TextField(_("why, what and how"), help_text=_("Blow us away with the details!"), blank=True)
    social_impact = models.TextField(_("social impact"), blank=True,help_text=_("Who are you helping?"))
    effects = models.TextField(_("effects"), help_text=_("What will be the Impact? How will your Smart Idea change the lives of people?"), blank=True)
    for_who = models.TextField(_("for who"), help_text=_("Describe your target group"), blank=True)
    future = models.TextField(_("future"), help_text=_("How will this project be self-sufficient and sustainable in the long term?"), blank=True)
    reach = models.PositiveIntegerField(_("Reach"), help_text=_("How many people do you expect to reach?"), blank=True, null=True)

    # Location
    latitude = models.DecimalField(_("latitude"), max_digits=21, decimal_places=18, null=True)
    longitude = models.DecimalField(_("longitude"), max_digits=21, decimal_places=18, null=True)
    country = models.ForeignKey('geo.Country', blank=True, null=True)

    # Media
    image = ImageField(_("image"), max_length=255, blank=True, upload_to='project_images/', help_text=_("Main project picture"))
    video_url = models.URLField(_("video"), max_length=100, blank=True, default='', help_text=_("Do you have a video pitch or a short movie that explains your project. Cool! We can't wait to see it. You can paste the link to the YouTube or Vimeo video here"))

    organization = models.ForeignKey('organizations.Organization', verbose_name=_("organisation"), blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('plan')
        verbose_name_plural = _('plans')


class PartnerOrganization(models.Model):
    """
        Some projects are run in cooperation with a partner
        organization like EarthCharter & MacroMicro
    """
    name = models.CharField(_("name"), max_length=255, unique=True)
    slug = models.SlugField(_("slug"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("partner organization")
        verbose_name_plural = _("partner organizations")

    def __unicode__(self):
        if self.name:
            return self.name
        return self.slug


# TODO: What is the for? Is is supposed to be reference? How is it related to Projects?
class Referral(models.Model):
    """
    People that are named as a referral.
    """
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email"))
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("referral")
        verbose_name_plural = _("referrals")


class BudgetLine(models.Model):
    """
    BudgetLine: Entries to the Project Budget sheet.
    This is the budget for the amount asked from this
    website.
    """
    project = models.ForeignKey(Project, verbose_name=_("project"))
    description = models.CharField(_("description"), max_length=255)
    money_amount = MoneyField(_("money amount"))

    class Meta:
        verbose_name = _("budget line")
        verbose_name_plural = _("budget lines")


# Now some stuff connected to Projects
# FIXME: Can we think of a better place to put this??
class Link(models.Model):
    """ Links (URLs) connected to a Project. """

    project = models.ForeignKey(Project, verbose_name=_("project"))
    name = models.CharField(_("name"), max_length=255)
    url = models.URLField(_("URL"))
    description = models.TextField(_("description"), blank=True)
    ordering = models.IntegerField(_("ordering"))
    created = CreationDateTimeField(_("created"))

    class Meta:
        ordering = ['ordering']
        verbose_name = _("link")
        verbose_name_plural = _("links")


class Testimonial(models.Model):
    """ Any user can write something nice about a project. """

    project = models.ForeignKey(Project, verbose_name=_("project"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"))
    description = models.TextField(_("description"))
    created = CreationDateTimeField(_("created"))
    updated = ModificationDateTimeField(_("updated"))

    class Meta:
        ordering = ['-created']
        verbose_name = _("testimonial")
        verbose_name_plural = _("testimonials")

    def __unicode__(self):
        return truncate_words(self.description, 20)


@receiver(post_save, weak=False, sender=Project)
def progress_project_phase(sender, instance, created, **kwargs):

    # If a new project is created it should have a pitch
    try:
        instance.projectpitch
    except ProjectPitch.DoesNotExist:
        instance.projectpitch = ProjectPitch(project=instance)
        instance.projectpitch.title = instance.title
        if instance.phase ==  ProjectPhases.pitch:
            instance.projectpitch.status = ProjectPitch.PitchStatuses.new
            instance.projectpitch.save()

    if instance.phase == ProjectPhases.pitch:
        try:
            instance.projectpitch.status = ProjectPitch.PitchStatuses.new
            instance.projectpitch.save()
        except ProjectPitch.DoesNotExist:
            pass
        try:
            instance.projectplan.status = ProjectPlan.PlanStatuses.new
        except ProjectPlan.DoesNotExist:
            pass

    # if phase progresses to 'plan' we should create and populate a ProjectPlan
    if instance.pk:
        if instance.phase == ProjectPhases.plan:
            # Create a ProjectPlan if it's not there yet
            try:
                instance.projectplan
            except ProjectPlan.DoesNotExist:
                instance.projectplan = ProjectPlan.objects.create(project=instance)
            if instance.projectpitch == None:
                Exception(_("There's no ProjectPitch for this Project. Can't create a ProjectPlan without a pitch."))
            for field in ['country', 'title', 'description', 'image', 'latitude', 'longitude', 'need', 'pitch', 'image',
                          'video_url', 'tags']:
                setattr(instance.projectplan, field, getattr(instance.projectpitch, field))

            # Set the correct statuses and save pitch and plan
            instance.projectplan.status = ProjectPlan.PlanStatuses.new
            instance.projectplan.save()

            if instance.projectpitch.status != ProjectPitch.PitchStatuses.approved:
                instance.projectpitch.status = ProjectPitch.PitchStatuses.approved
                instance.projectpitch.save()


@receiver(post_save, weak=False, sender=ProjectPitch)
def pitch_status_status(sender, instance, created, **kwargs):

    if instance.status == ProjectPitch.PitchStatuses.approved:
        instance.project.phase = ProjectPhases.plan
        instance.project.save()
