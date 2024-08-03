from django import forms

from webapp.models import Reply


class ReplyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Reply
        fields = ['content']