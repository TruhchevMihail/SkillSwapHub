from django import forms
from .models import SkillOffer, Material, SkillCategory


class SkillOfferBaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.setdefault('placeholder', 'e.g. Python basics for beginners')
        self.fields['description'].widget.attrs.setdefault(
            'placeholder',
            'Explain what learners will practice and who the session is for.',
        )
        self.fields['price_per_session'].widget.attrs.setdefault('placeholder', '35.00')
        self.fields['duration_minutes'].widget.attrs.setdefault('placeholder', '60')
        self.fields['category'].queryset = SkillCategory.objects.order_by('name')

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
    pass


class SkillOfferEditForm(SkillOfferBaseForm):
    pass


class SkillOfferFilterForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'placeholder': 'Search by title or keyword'})
        self.fields['category'].queryset = SkillCategory.objects.order_by('name')


class MaterialUploadForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('title', 'file')
