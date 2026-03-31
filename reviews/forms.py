from django import forms

from .models import Review

RATING_CHOICES = [(i, f'{i} / 5') for i in range(1, 6)]


class ReviewBaseForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label='Your rating',
    )

    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'comment': 'Your review',
        }
        help_texts = {
            'comment': 'Share your experience with this mentor and session.',
        }

    def clean_rating(self):
        return int(self.cleaned_data['rating'])

    def clean_comment(self):
        comment = self.cleaned_data['comment'].strip()
        if len(comment) < 10:
            raise forms.ValidationError('Comment must be at least 10 characters long.')
        return comment


class ReviewCreateForm(ReviewBaseForm):
    pass


class ReviewEditForm(ReviewBaseForm):
    pass

