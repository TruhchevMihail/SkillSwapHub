"""Forms for the offers app."""

from django import forms

from .models import SkillOffer, Material, SkillCategory


class SkillOfferBaseForm(forms.ModelForm):
    """Base form for creating and editing skill offers."""
    
    class Meta:
        model = SkillOffer
        fields = (
            'title',
            'description',
            'price_per_session',
            'duration_minutes',
            'level',
            'image',
            'category',
            'tags',
            'is_active',
        )
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'tags': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'title': 'Offer title',
            'description': 'Offer description',
            'price_per_session': 'Price per session',
            'duration_minutes': 'Session duration (minutes)',
            'is_active': 'Visible to users',
        }
        help_texts = {
            'title': 'Use a short, clear title.',
            'description': 'Describe what the learner will gain from the session.',
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()

        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')

        return title


class SkillOfferCreateForm(SkillOfferBaseForm):
    """Form for creating a new skill offer."""
    pass


class SkillOfferEditForm(SkillOfferBaseForm):
    """Form for editing an existing skill offer."""
    pass


class SkillOfferFilterForm(forms.Form):
    """Form for filtering and sorting skill offers."""
    
    search = forms.CharField(
        required=False,
        label='Search',
    )

    category = forms.ModelChoiceField(
        queryset=SkillCategory.objects.all(),
        required=False,
        empty_label='All categories',
    )

    level = forms.ChoiceField(
        choices=[('', 'All levels')] + SkillOffer.LEVEL_CHOICES,
        required=False,
    )

    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        max_digits=8,
        label='Maximum price',
    )

    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Newest first'),
            ('oldest', 'Oldest first'),
            ('price_asc', 'Price ascending'),
            ('price_desc', 'Price descending'),
        ],
    )


class MaterialUploadForm(forms.ModelForm):
    """Form for uploading materials to a skill offer."""
    
    class Meta:
        model = Material
        fields = ('title', 'file')

