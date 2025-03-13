from django.views import generic

from .queries import get_all_instructor, get_instructor_by_id_slug
from .utils import get_master_instructor_social_media
from ..carts.carts import Cart


class InstructorListView(generic.ListView):
    template_name = 'instructors/instructor_list.html'
    context_object_name = 'instructors'
    queryset = get_all_instructor()


class InstructorDetailView(generic.DetailView):
    template_name = 'instructors/instructor_detail.html'
    context_object_name = 'instructor'

    def get_queryset(self):
        return get_instructor_by_id_slug(self.kwargs['pk'], self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(InstructorDetailView, self).get_context_data(**kwargs)

        # social media IDs of the master coach
        master_social_media = get_master_instructor_social_media()
        if master_social_media:
            context.update(master_social_media)

        # user cart items
        cart = Cart(self.request)
        cart_items = [(item['id'], item['type']) for item in cart.cart]
        context['carts'] = cart_items
        return context
