from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review Title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience...'
            }),
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(1, 6)], attrs={
                'class': 'form-select'
            }),
        }
