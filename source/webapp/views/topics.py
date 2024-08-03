from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView

from webapp.forms.replies import ReplyForm
from webapp.forms.topics import TopicForm
from webapp.models import Topic, Reply


# Create your views here.
class TopicListView(ListView):
    model = Topic
    template_name = 'topics/home.html'


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
