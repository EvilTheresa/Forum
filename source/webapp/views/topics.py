from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView

from webapp.forms.replies import ReplyForm
from webapp.forms.search_form import SearchForm
from webapp.forms.topics import TopicForm
from webapp.models import Topic, Reply


# Create your views here.
class TopicListView(ListView):
    model = Topic
    template_name = 'topics/home.html'
    paginate_by = 7

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        form = self.form
        if form.is_valid():
            return form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(name__contains=self.search_value) | Q(description__contains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        if self.search_value:
            context["search"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
        return context


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'topics/detail_topic.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReplyForm()
        context['replies'] = Reply.objects.filter(topic=self.get_object())
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    template_name = "topics/create_topic.html"
    form_class = TopicForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TopicUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "topics/update_topic.html"
    context_object_name = 'topic'
    permission_required = "webapp.change_topic"

    def get_success_url(self):
        return reverse_lazy('webapp:project_detail', kwargs={'pk': self.object.project.pk})

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().user


class TopicDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = "topics/delete_topic.html"
    context_object_name = 'topic'
    permission_required = "webapp.delete_topic"

    def get_success_url(self):
        return reverse_lazy('webapp:project_detail', kwargs={'pk': self.object.project.pk})

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().user
