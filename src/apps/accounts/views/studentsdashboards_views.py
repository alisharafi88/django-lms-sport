from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

from jalali_date import datetime2jalali

from ..forms import EditProfileForm
from apps.carts.carts import Cart
from apps.courses.models import Course
from ...tickets.models import Ticket


class StudentsDashboard(LoginRequiredMixin, View):
    template_name = 'accounts/dashboards/student_dashboard.html'
    
    def get(self, request):
        # Student Courses
        courses_queryset = Course.objects.filter(memberships__user=request.user.id, status=True)

        # Cart
        cart = Cart(request)
        total_price, total_discounted_price = cart.get_total_price()

        # Ticket
        ticket_queryset = Ticket.objects.prefetch_related('replies').filter(user=request.user)

        # Edit Profile
        edit_profile_form = EditProfileForm(instance=request.user)

        context = {
            # Cart
            'carts': cart,
            'total_price': total_price,
            'total_discounted_price': total_discounted_price,

            # Student Courses
            'courses': courses_queryset,

            # Ticket
            'tickets': ticket_queryset,

            # Edit Profile
            'edit_profile_form': edit_profile_form,
        }

        return render(
            request,
            self.template_name,
            context,
        )


class StudentEditProfileView(LoginRequiredMixin, View):
    def post(self, request):
        edit_profile_form = EditProfileForm(request.POST, instance=request.user, files=request.FILES)
        if edit_profile_form.is_valid():
            if request.POST.get('remove_profile_photo') == "true":
                request.user.profile_photo = None
            edit_profile_form.save()

            profile_photo_url = request.user.profile_photo.url if request.user.profile_photo else None
            full_name = str(request.user.get_name)
            return JsonResponse({
                "success": True,
                "message": _("Your changes have been saved."),
                "profile_photo_url": profile_photo_url,
                "has_uploaded_photo": bool(request.user.profile_photo),
                "full_name": full_name,
            })

        return JsonResponse({
            "success": False,
            "message": _("Something went wrong. Please try again."),
            "errors": edit_profile_form.errors,
        }, status=400)


class TicketCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ticket
    fields = ['subject', 'message']

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': _('You must be logged in to create a ticket.')})

        first_name = request.POST.get('firstName').strip()
        last_name = request.POST.get('lastName').strip()
        message = request.POST.get('message').strip()
        subject = request.POST.get('subject').strip()

        if not first_name or not last_name or not message:
            return JsonResponse({'success': False, 'message': _('All fields are required.')})

        try:
            user = request.user
            if first_name and last_name:
                user.first_name = first_name
                user.last_name = last_name
                user.save()

            ticket = Ticket.objects.create(
                user=user,
                subject=subject,
                message=message,
            )

            return JsonResponse({
                'success': True,
                'message': _('Ticket created successfully.'),
                'ticket': {
                    'id': ticket.id,
                    'subject': ticket.subject,
                    'status': ticket.get_status_display(),
                    'date_updated': datetime2jalali(ticket.date_updated).strftime('%Y-%m-%d , %H:%M:%S'),
                    'message': ticket.message,
                    'replies': []
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
