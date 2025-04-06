from django.views import generic

from .queries import get_all_instructor, get_instructor_by_id_slug
from .utils import get_master_instructor_social_media
from ..carts.carts import Cart
from ..courses.models import CourseMembership


class InstructorListView(generic.ListView):
    template_name = 'instructors/instructor_list.html'
    context_object_name = 'instructors'

    def get_queryset(self):
        queryset = get_all_instructor()
        return queryset


class InstructorDetailView(generic.DetailView):
    template_name = 'instructors/instructor_detail.html'
    context_object_name = 'instructor'

    def get_queryset(self):
        return get_instructor_by_id_slug(self.kwargs['pk'], self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(InstructorDetailView, self).get_context_data(**kwargs)

        # user cart items
        cart = Cart(self.request)
        cart_items = [(item['id'], item['type']) for item in cart.cart]
        context['carts'] = cart_items

        # user enrollment
        if self.request.user.is_authenticated:
            memberships = CourseMembership.objects.filter(user=self.request.user).select_related('content_type')
            user_memberships = {(m.content_type_id, m.object_id): True for m in memberships}
        else:
            user_memberships = {}

        context['user_memberships'] = user_memberships
        return context
