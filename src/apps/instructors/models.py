from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name=_('user'),)
    slug = models.SlugField(_('slug'), blank=True, allow_unicode=True,)
    description = models.TextField(_('description'), help_text=_('Provide a detailed description of the instructor.'),)
    experience = models.PositiveIntegerField(_('experience'), help_text=_('Enter the number of years of experience.'),)

    telegram_id = models.CharField(max_length=50, blank=True, null=True, help_text=_('Enter your Telegram ID to display on your profile.'),)
    youtube_id = models.CharField(max_length=50, blank=True, null=True, help_text=_('Enter your YouTube ID to display on your profile.'),)
    instagram_id = models.CharField(max_length=50, blank=True, null=True, help_text=_('Enter your Instagram ID to display on your profile.'),)

    img = models.ImageField(upload_to='instructors/imgs/',)

    is_master = models.BooleanField(_('is master'), default=False, help_text=_('Check this box to set master instructor and display social media links.'),)
    is_active = models.BooleanField(_('is active'), default=True, help_text=_('Check this box to set this instructor as active.'),)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_absolute_url(self):
        return reverse('instructors:instructor_detail', kwargs={'pk': self.pk, 'slug': self.slug},)

    def save(self, *args, **kwargs):
        # Generate a URL-friendly slug from the instructor's full name
        self.slug = slugify(self.full_name, allow_unicode=True)

        # Ensure only one instructor can be marked as master
        if self.is_master:
            Instructor.objects.filter(is_master=True).update(is_master=False)

        super(Instructor, self).save(*args, **kwargs)


class InstructorWidjet(models.Model):
    instructor = models.ForeignKey(
        settings.INSTRUCTOR_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('instructor widjet'),
        related_name='widjets',
    )
    widjet = models.CharField(verbose_name=_('widjet'), max_length=20, help_text=_('short Widjet'))

    def __str__(self):
        return self.widjet


class InstructorHonor(models.Model):
    instructor = models.ForeignKey(
        settings.INSTRUCTOR_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('instructor'),
        related_name='honors',
        help_text=_('add your honor here, with one related photo'),
    )
    text = models.CharField(verbose_name=_('honor'), max_length=50, )
    img = models.ImageField(_('photo'), upload_to='instructors/honor/img', )

    status = models.BooleanField(_('status'), default=True, )
