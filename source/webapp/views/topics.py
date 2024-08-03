from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView


# Create your views here.
class TopicListView(ListView):
    model = Topic
    template_name = 'topics/home.html'


class TopicDetailView(TemplateView):
    template_name = "topics/detail_topic.html"

    def dispatch(self, request, *args, **kwargs):
        self.topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['topic'] = self.topic
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    template_name = "topics/add_topic.html"
    form_class = TopicForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        topic = form.save(commit=False)
        topic.project = project
        topic.save()
        return redirect("webapp:project_detail", pk=self.kwargs['pk'])


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
