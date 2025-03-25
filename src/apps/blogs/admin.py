from django.contrib import admin
from django.db import models
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from jalali_date.admin import ModelAdminJalaliMixin, TabularInlineJalaliMixin
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Blog, BlogComment


class BlogCommentInline(TabularInlineJalaliMixin, admin.TabularInline):
    model = BlogComment
    readonly_fields = ('date_created',)
    fields = ('author', 'text', 'date_created')
    extra = 0


@admin.register(Blog)
class BlogAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }
    list_display = ('title', 'author', 'status', 'num_of_comments')
    list_filter = ('title', 'author', 'status',)
    list_per_page = 10
    list_editable = ('status',)
    search_fields = ('title', 'author',)
    date_hierarchy = 'date_updated'
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('date_created', 'date_updated',)
    inlines = (BlogCommentInline,)
    fieldsets = (
        (None, {'fields': ('title', 'description', 'slug', 'img',)}),
        (None, {'fields': ('author',)}),
        ('status', {'fields': ('status', 'enable_comments',)}),
        ('Date information', {'fields': ('date_created', 'date_updated',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('title', 'description', 'slug', 'img',)}),
        (None, {'fields': ('author',)}),
        ('status', {'fields': ('status', 'enable_comments',)}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        return super().get_queryset(request)\
            .prefetch_related('comments')\
            .annotate(num_of_comments=Count('comments'))

    @admin.display(description=_('#comments'), ordering='-num_of_comments')
    def num_of_comments(self, blog):
        return blog.comments.all().count()


admin.site.register(BlogComment)
