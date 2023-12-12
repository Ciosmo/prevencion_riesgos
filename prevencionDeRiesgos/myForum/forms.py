from django import forms
from .models import Author


class ProfilePicUpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname','profilePic', 'bio']