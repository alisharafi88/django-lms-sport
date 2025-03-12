from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _

from django_ckeditor_5.fields import CKEditor5Field


class Blog(models.Model):
    BLOG_STATUS_PUBLISHED = "p"
    BLOG_STATUS_REJECT = 'r'
    BLOG_STATUS_CHOICES = (
        (BLOG_STATUS_PUBLISHED, _("Published")),
        (BLOG_STATUS_REJECT, _("Rejected"))
    )

    author = models.ForeignKey(
        settings.INSTRUCTOR_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blogs',
    )
    title = models.CharField(_("Blog's title"), max_length=400, )
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = CKEditor5Field(verbose_name=_("blog's description"), )

    img = models.ImageField(_("Blog's main img"), upload_to="blogs/%Y/%m/%d", )

    status = models.CharField(
        max_length=1,
        choices=BLOG_STATUS_CHOICES,
        default=BLOG_STATUS_PUBLISHED,
        verbose_name=_("Blog's status"),
    )
    enable_comments = models.BooleanField(verbose_name=_("Enable comments on post"), default=True, )

    date_created = models.DateTimeField(_("Created at"), auto_now_add=True, )
    date_updated = models.DateTimeField(_("Updated at"), auto_now=True, )

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
        ordering = ('-date_updated',)

    def __str__(self):
        return f'{self.title} - {self.author} - {self.status}'

    def get_absolute_url(self):
        return reverse('blogs:blog_detail', kwargs={'pk': self.pk, 'slug': self.slug})


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Blog's comments"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_blogs_comments',
        verbose_name="Comment's author",
    )
    text = models.CharField(_("Comment's text"), max_length=500, )

    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True,
                               verbose_name=_('Parent'), )

    status = models.BooleanField(_('Status'), default=True,
                                 help_text=_('If the comment is not appropriate, set it to false.'))

    date_created = models.DateTimeField(_("created at"), auto_now_add=True, )

    class Meta:
        verbose_name = _("Blog comment")
        verbose_name_plural = _("Blog comments")
        ordering = ('-date_created',)

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def __str__(self):
        return f'{self.blog} - {self.author}'
