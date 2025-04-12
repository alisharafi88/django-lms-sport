from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field


def upload_introduce_video_path(instance, filename):
    return f'course/introduce/videos/{instance.slug}/{filename}'


def upload_introduce_video_cover_path(instance, filename):
    return f'course/introduce/videos/covers/{instance.slug}/{filename}'


def upload_introduce_image_path(instance, filename):
    return f'course/introduce/image/{instance.slug}/{filename}'


class Coupon(models.Model):
    """
    Coupon for courses or packages.
    """
    code = models.CharField(
        _('Coupon Code'),
        max_length=50,
        unique=True,
    )
    discount_amount = models.PositiveIntegerField(
        _('Discount Amount'),
        default=0,
        help_text=_('The amount of discount (in currency units).'),
    )
    date_valid_from = models.DateField(
        _('Valid From'),
    )
    date_valid_to = models.DateField(
        _('Valid To'),
    )
    status = models.BooleanField(
        _('Status'),
        default=True,
        help_text=_('Whether the coupon is active or not.'),
    )
    max_usage_per_user = models.IntegerField(
        _('Max Usage Per User'),
        default=1,
        help_text=_('Maximum number of times a user can use this coupon.'),
    )
    max_usage_total = models.IntegerField(
        _('Max Total Usage'),
        default=100,
        help_text=_('Maximum number of times the coupon can be used globally.'),
    )

    def __str__(self):
        return f'{self.code} - {self.discount_amount}'

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')


class CouponUsage(models.Model):
    """
    Tracks usage of coupons by users.
    """
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        related_name='usages',
        verbose_name=_('Coupon'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='coupon_usages',
        verbose_name=_('User'),
    )
    usage_date = models.DateTimeField(
        _('Usage Date'),
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.coupon.code} on {self.usage_date}'

    class Meta:
        verbose_name = _('Coupon Usage')
        verbose_name_plural = _('Coupon Usages')


class Product(models.Model):
    title = models.CharField(
        _('Title'),
        max_length=100,
        db_index=True,
    )
    slug = models.SlugField(
        _('Slug'),
        unique=True,
        allow_unicode=True,
    )

    description = CKEditor5Field(
        verbose_name=_("Description")
    )

    price = models.PositiveIntegerField(
        _('Price'),
        default=0,
    )
    discount_amount = models.PositiveIntegerField(
        _('Discount amount'),
        default=0,
        help_text=_('Discount amount for this product.'),
    )

    img = models.ImageField(_("Main Image"), upload_to=upload_introduce_image_path)

    introduce_video_cover = models.ImageField(_('Video\'s Cover'), help_text=_('Cover of introduce video'), upload_to=upload_introduce_video_cover_path, blank=True, null=True)
    introduce_video_url = models.URLField(_('Introduce Video URL'), blank=True, null=True)

    age_range = models.CharField(_('Age range'), max_length=12, help_text=_('Age range for users.'))
    duration = models.CharField(_('Duration'), max_length=10, help_text=_('How long it takes to complete this course?.'))

    date_created = models.DateTimeField(_('Date created at'), auto_now_add=True, db_index=True)
    date_modified = models.DateTimeField(_('Date modified at'), auto_now=True, db_index=True)

    status = models.BooleanField(_('Status'), default=True, help_text=_('Show that this product is active or not.'), db_index=True)

    certificate_status = models.BooleanField(_('Certificate'), help_text=_('Show that this course have certificate or no.'), default=False)
    analysis_room_status = models.BooleanField(_('Analysis room'), default=False)
    extra_movments_status = models.BooleanField(_('Extra movments'), default=False)
    injury_prevention_status = models.BooleanField(_('Injury prevention'), default=False)

    class Meta:
        abstract = True
        indexes = [
            models.Index(
                fields=['status', '-date_created'],
                name='%(class)s_status_created_idx'
            ),
            models.Index(
                fields=['price', 'status'],
                name='%(class)s_price_status_idx'
            ),

            models.Index(
                fields=['status'],
                name='%(class)s_status_covering_idx'
            )
        ]

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
        db_index=True,
    )

    free_leasson_link = models.URLField(
        _('Free leasson link'),
        unique=True,
        null=True,
        blank=True,
    )
    memberships = GenericRelation('CourseMembership', related_query_name='course')

    is_featured_on_homepage = models.BooleanField(
        _('Featured on Homepage'),
        default=False,
        help_text=_('Only one course can be featured on the homepage at a time.')
    )

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})

    def clean(self):
        """
        Ensure only one course can be featured on the homepage at a time.
        """
        if self.is_featured_on_homepage:
            if Course.objects.filter(is_featured_on_homepage=True).exclude(pk=self.pk).exists():
                raise ValidationError(_('Only one course can be featured on the homepage at a time.'))

    class Meta(Product.Meta):
        indexes = Product.Meta.indexes + [
            models.Index(
                fields=['coach', 'status'],
                name='course_coach_status_idx'
            )
        ]

        verbose_name = _('Course')
        verbose_name_plural = _('Courses')


class Package(Product):
    courses = models.ManyToManyField(Course, verbose_name=_('Courses in this package'))

    memberships = GenericRelation('CourseMembership', related_query_name='package')

    def get_absolute_url(self):
        return reverse('courses:package_detail', kwargs={'slug': self.slug})

    class Meta(Product.Meta):
        indexes = Product.Meta.indexes + [
            models.Index(
                fields=['certificate_status', 'status'],
                name='package_cert_status_idx'
            )
        ]

        verbose_name = _('Package')
        verbose_name_plural = _('Packages')


class CourseSeason(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='seasons',
        verbose_name=_('Course'),
    )

    title = models.CharField(_('Title'), max_length=100)

    created_at = models.DateTimeField(_('Creat Date'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Update Date'), auto_now=True)

    def __str__(self):
        return f'{self.course} - {self.title}'

    class Meta:
        ordering = ('created_at',)

        verbose_name = _('Season')
        verbose_name_plural = _('Seasons')


class CourseVideo(models.Model):
    class VideoStatus(models.TextChoices):
        FREE = 'f', _('Free')
        MONETARY = 'm', _('Monetary')

    season = models.ForeignKey(
        CourseSeason,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name=_('Season'),
    )

    title = models.CharField(_('title'), max_length=100, )

    status = models.CharField(
        _('Status'), max_length=1,
        choices=VideoStatus.choices,
        default=VideoStatus.MONETARY,
        help_text=_('Show that this video is free or not.'),
    )

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def is_free(self):
        if self.status == self.VideoStatus.FREE:
            return True
        return False

    def __str__(self):
        return f'{self.season} - {self.title}'

    class Meta:
        ordering = ('created_at',)
        indexes = (
            models.Index(fields=['season'], name='courses_video_season_idx'),
            models.Index(fields=['created_at'], name='courses_video_created_at_idx'),
        )

        verbose_name = _('Video')
        verbose_name_plural = _('Videos')


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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_comments',
        verbose_name=_('User'),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Course')
    )
    text = models.TextField(_('Text of the comment'), )
    rate = models.PositiveSmallIntegerField(
        _('Rate'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    date_created = models.DateTimeField(
        _('Created date'),
        auto_now_add=True,
    )

    status = models.BooleanField(
        _('Status'),
        default=True,
        help_text=_('If the comment is not appropriate, set it to false.')
    )

    class Meta:
        ordering = ('-date_created',)

        verbose_name = _('course\'s comment')
        verbose_name_plural = _('course\'s comments')

    @property
    def is_member(self):
        if self.user.id in [member.id for member in self.course.members]:
            return True
        return False

    def __str__(self):
        return f'{self.user} - {self.course.title}'


class CourseTelegramLink(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='telegram_links',
        verbose_name=_('Course')
    )
    invite_link = models.URLField(
        _('Telegram Invite Link'),
        unique=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='telegram_links',
        verbose_name=_('Assigned User')
    )
    is_used = models.BooleanField(_('Used'), default=False)

    date_created = models.DateTimeField(_('Create Date'), auto_now_add=True)
    date_used = models.DateTimeField(_('Update Date'), blank=True, null=True)

    class Meta:
        verbose_name = _('Telegram Link')
        verbose_name_plural = _('Telegram Links')

    def __str__(self):
        if self.user:
            return f'{self.course.title} - {self.invite_link}'
        return self.course.title
