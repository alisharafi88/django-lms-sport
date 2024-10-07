"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls,),
    path('', include('home.urls', namespace='home'),),
    path('courses/', include('courses.urls', namespace='courses'),),
    path('blogs/', include('blogs.urls', namespace='blogs'),),
    path('faq/', include('faq.urls', namespace='faq'),),
    path('contact/', include('contacts.urls', namespace='contacts'),),
    path('instructors/', include('instructors.urls', namespace='instructors'),),
    path('carts/', include('carts.urls', namespace='carts'),),
    path('orders/', include('orders.urls', namespace='orders'),),
    path('accounts/', include('accounts.urls', namespace='accounts')),
] + debug_toolbar_urls()

urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls'),),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
