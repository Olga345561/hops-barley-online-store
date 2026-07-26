from django import forms
from .models import CommunityPost


class CommunityPostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a post title...'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us about your experience or recipe...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }