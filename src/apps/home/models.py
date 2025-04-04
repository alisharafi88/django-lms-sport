from django.db import models
from django.utils.translation import gettext_lazy as _


class Counter(models.Model):
    students = models.IntegerField(_('Students'), default=7000)
    experience_years = models.IntegerField(_('Experience years'), default=14)
    professional_courses = models.IntegerField(_('Professional Courses'), default=8)
    comments = models.IntegerField(_('Comments'), default=5)

    def __str__(self):
        return "Global Counter"

    def save(self, *args, **kwargs):
        # Force ID to 1 to enforce singleton
        self.id = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

    class Meta:
        verbose_name = _('Counter')
        verbose_name_plural = _('Counter')
