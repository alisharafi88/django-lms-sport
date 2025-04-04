from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CourseMembership, Course, CourseComments
from ..home.models import Counter


@receiver(post_save, sender=CourseMembership)
def increment_student_counter(sender, instance, created, **kwargs):
    if created:
        counter = Counter.load()
        counter.students += 1
        counter.save()


@receiver(post_save, sender=Course)
def increment_professional_courses_counter(sender, instance, created, **kwargs):
    if created:
        counter = Counter.load()
        counter.professional_courses += 1
        counter.save()


@receiver(post_save, sender=CourseComments)
def increment_professional_courses_counter(sender, instance, created, **kwargs):
    if created:
        counter = Counter.load()
        counter.comments += 1
        counter.save()
