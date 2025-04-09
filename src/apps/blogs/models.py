from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field


class Blog(models.Model):
    BLOG_STATUS_PUBLISHED = 'p'
    BLOG_STATUS_REJECT = 'r'
    BLOG_STATUS_CHOICES = (
        (BLOG_STATUS_PUBLISHED, _('Published')),
        (BLOG_STATUS_REJECT, _('Rejected'))
    )

    author = models.ForeignKey(
        settings.INSTRUCTOR_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blogs',
        verbose_name=_('Author')
    )
    title = models.CharField(_('Title'), max_length=400, )
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = CKEditor5Field(verbose_name=_('Description'), )

    img = models.ImageField(_('Image'), upload_to='blogs/%Y/%m/%d', )

    status = models.CharField(
        max_length=1,
        choices=BLOG_STATUS_CHOICES,
        default=BLOG_STATUS_PUBLISHED,
        verbose_name=_('Status'),
    )
    enable_comments = models.BooleanField(
        verbose_name=_('Enable comments'),
        help_text=_('If checked, users will be able to post comments on this content.'),
        default=True,
    )

    date_created = models.DateTimeField(_('Created at'), auto_now_add=True, )
    date_updated = models.DateTimeField(_('Updated at'), auto_now=True, )

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
        ordering = ('-date_updated',)

    def __str__(self):
        return f'{self.title} - {self.author}'

    def get_absolute_url(self):
        return reverse('blogs:blog_detail', kwargs={'pk': self.pk, 'slug': self.slug})


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Blog'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_blogs_comments',
        verbose_name=_('Author'),
    )
    text = models.CharField(_('Text'), max_length=500, )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        blank=True,
        null=True,
        verbose_name=_('Replayed to'),
    )

    status = models.BooleanField(
        _('Status'),
        default=True,
        help_text=_('If the comment is not appropriate, set it to false.'),
    )

    date_created = models.DateTimeField(_('created at'), auto_now_add=True, )

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ('-date_created',)

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return f'{self.blog} - {self.author}'
