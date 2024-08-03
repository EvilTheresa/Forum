from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from accounts.forms import MyUserCreationForm

User = get_user_model()


class RegistrationView(CreateView):
    form_class = MyUserCreationForm
    template_name = "registration.html"
    model = User

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:topics')
        return next_url


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user_profile.html"
    context_object_name = "user_obj"
    paginate_related_by = 3

    def get_context_data(self, **kwargs):
        topics = self.object.topics.order_by('-created_at')
        paginator = Paginator(topics, self.paginate_related_by)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['topics'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)
