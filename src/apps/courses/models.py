from django.core.validators import FileExtensionValidator
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _
from django_ckeditor_5.fields import CKEditor5Field


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


class Course(models.Model):
    instructor = models.ForeignKey(settings.INSTRUCTOR_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses',
                                   verbose_name=_('instructor'), )
    parent = models.ManyToManyField('self', symmetrical=False, blank=True, verbose_name=_('Courses'))

    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = CKEditor5Field(verbose_name=_("description"), )

    age_range = models.CharField(_('age range'), max_length=50, help_text=_('Age range for users.'))
    duration = models.CharField(_('duration'), max_length=10,
                                help_text=_('How long it takes to complete this course?.'))

    img = models.ImageField(_("main img"), upload_to="courses/%Y/%m/%d", )

    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=5, decimal_places=2, default=0.00,
                                          help_text=_('Discount amount for course.'))

    date_created = models.DateTimeField(_('date created at'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified at'), auto_now=True)

    status = models.BooleanField(_('status'), default=True, help_text='Show that this course is active or no.')

    certificate_status = models.BooleanField(_('certificate'),
                                             help_text='Show that this course have certificate or no.', default=False)
    analysis_room_status = models.BooleanField(_('analysis room'), default=False)
    extra_movments_status = models.BooleanField(_('extra movments'), default=False)
    injury_prevention_status = models.BooleanField(_('injury prevention'), default=False)

    def discounted_price(self):
        """
        Returns the discounted price
        """
        return self.price - self.discount_amount

    @property
    def is_package(self):
        return self.parent.exists()

    def __str__(self):
        return f'{self.title} - {self.price} - {self.status}'

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'pk': self.pk, 'slug': self.slug})


class CourseVideo(models.Model):
    VIDEO_STATUS_NOT_FREE = 'm'
    VIDEO_STATUS_FREE = 'f'
    VIDEO_STATUS_CHOICES = (
        (VIDEO_STATUS_NOT_FREE, _('Monetary')),
        (VIDEO_STATUS_FREE, _('Free')),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos', verbose_name=_('course'), )
    title = models.CharField(_('title'), max_length=100, )
    slug = models.SlugField(blank=True, null=True, )
    video = models.FileField(
        upload_to='course_videos',
        verbose_name=_('Course video'),
        help_text='Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3',
        validators=[FileExtensionValidator(['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3', ])],
    )

    status = models.CharField(_('status'), max_length=1, choices=VIDEO_STATUS_CHOICES, default=VIDEO_STATUS_NOT_FREE,
                              help_text='Show that this video is free or not.', )

    def __str__(self):
        return str(self.title)


class CourseMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses',
                             verbose_name=_('Curse membership'), )
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='members',
                               verbose_name=_('Course'), )

    date_created = models.DateTimeField(_('Created date'), auto_now_add=True, )
    date_modified = models.DateTimeField(_('Modified date'), auto_now=True, )

    class Meta:
        unique_together = ('user', 'course',)

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'


class CourseComments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_comments',
                             verbose_name=_('User'), )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Course'))
    text = models.TextField(_('Text of the comment'), )
    date_created = models.DateTimeField(_('Created date'), auto_now_add=True, )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True,
                               verbose_name=_('Parent'), )

    status = models.BooleanField(_('Status'), default=True,
                                 help_text=_('If the comment is not appropriate, set it to false.'))

    class Meta:
        ordering = ('-date_created',)

    @property
    def is_member(self):
        if self.user.id in [member.id for member in self.course.members]:
            return True
        return False

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        if self.is_parent:
            return f'{self.user} - {self.course.title}'
        return f'{self.user} - {self.parent.user} - {self.course.title}'
