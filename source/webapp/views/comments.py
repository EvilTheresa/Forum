from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from webapp.forms.replies import ReplyForm
from webapp.models import Topic, Reply


class CreateReplyView(LoginRequiredMixin, CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'replies/create_reply.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.topic = Topic.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('webapp:topic_detail', kwargs={'pk': self.kwargs.get('pk')})


class UpdateReplyView(UpdateView):
    template_name = "replies/update_reply.html"
    form_class = ReplyForm
    model = Reply

    def get_success_url(self):
        return reverse("webapp:article_detail", kwargs={"pk": self.object.article.pk})


class DeleteReplyView(DeleteView):
    queryset = Reply.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("webapp:article_detail", pk=self.object.article.pk)
