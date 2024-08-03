from django import forms

from webapp.models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']