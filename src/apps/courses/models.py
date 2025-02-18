from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _
from django_ckeditor_5.fields import CKEditor5Field


def upload_introduce_video_path(instance, filename):
    return f'course/introduce/videos/{instance.slug}/{filename}'


def upload_introduce_image_path(instance, filename):
    return f'course/introduce/image/{instance.slug}/{filename}'


class Coupon(models.Model):
    """
    Coupon for courses
    """
    code = models.CharField(_('code of coupon'), max_length=50, unique=True)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=5, decimal_places=2)
    date_valid_from = models.DateField(_('date valid from'), )
    date_valid_to = models.DateField(_('date valid to'), )
    status = models.BooleanField(_('status'), default=True)
    max_usage_per_user = models.IntegerField(_('max number of usage'), default=1,
                                             help_text='Number of people who can use.')

    def __str__(self):
        return f'{self.date_valid_to} - {self.discount_amount}'


class Product(models.Model):
    title = models.CharField(_('Title'), max_length=100)
    slug = models.SlugField(unique=True, allow_unicode=True)

    description = CKEditor5Field(verbose_name=_("Description"))

    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(
        _('Discount amount'),
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text=_('Discount amount for this product.'),
    )

    img = models.ImageField(_("Main img"), upload_to=upload_introduce_image_path, )
    introduce_video = models.FileField(_('Introduce Video'), upload_to=upload_introduce_video_path, blank=True, null=True)

    age_range = models.CharField(_('Age range'), max_length=50, help_text=_('Age range for users.'))

    date_created = models.DateTimeField(_('Date created at'), auto_now_add=True)
    date_modified = models.DateTimeField(_('Date modified at'), auto_now=True)

    status = models.BooleanField(_('Status'), default=True, help_text=_('Show that this product is active or not.'))

    certificate_status = models.BooleanField(_('Certificate'), help_text=_('Show that this course have certificate or no.'), default=False)
    analysis_room_status = models.BooleanField(_('Analysis room'), default=False)
    extra_movments_status = models.BooleanField(_('Extra movments'), default=False)
    injury_prevention_status = models.BooleanField(_('Injury prevention'), default=False)

    class Meta:
        abstract = True

    def discounted_price(self):
        return self.price - self.discount_amount

    def __str__(self):
        return self.title


class Course(Product):
    coach = models.ForeignKey(
        settings.INSTRUCTOR_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name=_('Coach'),
    )

    duration = models.CharField(_('Duration'), max_length=10, help_text=_('How long it takes to complete this course?.'))

    memberships = GenericRelation('CourseMembership', related_query_name='course')

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'pk': self.pk, 'slug': self.slug})


class Package(Product):
    courses = models.ManyToManyField(Course, verbose_name=_('Courses in this package'))

    memberships = GenericRelation('CourseMembership', related_query_name='package')

    # def get_absolute_url(self):
    #     return reverse('courses:package_detail', kwargs={'pk': self.pk, 'slug': self.slug})


class CourseSeason(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_('Course'),
        related_name='seasons',
    )

    title = models.CharField(_('Title'), max_length=100)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        return f'{self.course} - {self.title}'

    class Meta:
        verbose_name = _('Season')
        verbose_name_plural = _('Seasons')
        ordering = ('created_at',)


class CourseVideo(models.Model):
    class VideoStatus(models.TextChoices):
        FREE = 'f', _('Free')
        MONETARY = 'm', _('Monetary')

    season = models.ForeignKey(
        CourseSeason,
        on_delete=models.CASCADE,
        verbose_name=_('Season'),
        related_name='videos',
    )

    title = models.CharField(_('title'), max_length=100, )

    status = models.CharField(
        _('Status'), max_length=1,
        choices=VideoStatus.choices,
        default=VideoStatus.MONETARY,
        help_text='Show that this video is free or not.',
    )

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        return f'{self.season} - {self.title}'

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
        ordering = ('created_at',)
        indexes = (
            models.Index(fields=['season'], name='courses_video_season_idx'),
            models.Index(fields=['created_at'], name='courses_video_created_at_idx'),
        )


class CourseMembership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name=_('User Membership'),
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ('course', 'package')},
        verbose_name=_('Content Type'),
    )
    object_id = models.PositiveIntegerField(verbose_name=_('Object ID'))
    product = GenericForeignKey('content_type', 'object_id')
    date_created = models.DateTimeField(_('Created Date'), auto_now_add=True)
    date_modified = models.DateTimeField(_('Modified Date'), auto_now=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        verbose_name = _('Course Membership')
        verbose_name_plural = _('Course Memberships')

    def __str__(self):
        return f'{self.user.get_name} - {self.product.title}'


class CourseComments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_comments',
                             verbose_name=_('User'), )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Course'))
    text = models.TextField(_('Text of the comment'), )
    rate = models.PositiveSmallIntegerField(_('Rate'), validators=[MinValueValidator(1), MaxValueValidator(5)])

    date_created = models.DateTimeField(_('Created date'), auto_now_add=True, )

    status = models.BooleanField(_('Status'), default=True,
                                 help_text=_('If the comment is not appropriate, set it to false.'))

    class Meta:
        ordering = ('-date_created',)

    @property
    def is_member(self):
        if self.user.id in [member.id for member in self.course.members]:
            return True
        return False

    def __str__(self):
        return f'{self.user} - {self.course.title}'
