from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

from ..forms import EditProfileForm
from apps.carts.carts import Cart
from apps.courses.models import Course


class StudentsDashboard(LoginRequiredMixin, View):
    template_name = 'accounts/dashboards/student_dashboard.html'
    
    def get(self, request):
        # Student Courses
        courses_queryset = Course.objects.filter(members__user=request.user.id, status=True)

        # Cart
        cart = Cart(request)
        total_price, total_discounted_price = cart.get_total_price()

        # Edit Profile
        edit_profile_form = EditProfileForm(instance=request.user)

        context = {
            # Cart
            'carts': cart,
            'total_price': total_price,
            'total_discounted_price': total_discounted_price,

            # Student Courses
            'courses': courses_queryset,

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
            full_name = request.user.get_full_name() if request.user.first_name or request.user.last_name else request.user.phone_number
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
