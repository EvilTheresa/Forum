from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from webapp.forms.replies import ReplyForm
from webapp.models import Topic, Reply


class CreateReplyView(LoginRequiredMixin, CreateView):
    template_name = "replies/create_reply.html"
    form_class = ReplyForm

    def form_valid(self, form):
        topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        reply = form.save(commit=False)
        reply.article = topic
        reply.author = self.request.user
        reply.save()
        return redirect(topic.get_absolute_url())


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
