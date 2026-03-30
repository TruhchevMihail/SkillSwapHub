from django import forms

from .models import Booking


class BookingCreateForm(forms.ModelForm):
    preferred_date = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Preferred date and time',
    )

    class Meta:
        model = Booking
        fields = ('preferred_date', 'message')
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'message': 'Additional message',
        }
        help_texts = {
            'message': 'Optional: add more information for the mentor.',
        }

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        return message


class BookingStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('status',)
        labels = {
            'status': 'Update booking status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        allowed_statuses = [
            Booking.Status.APPROVED,
            Booking.Status.REJECTED,
            Booking.Status.COMPLETED,
        ]

        self.fields['status'].choices = [
            (choice_value, choice_label)
            for choice_value, choice_label in Booking.Status.choices
            if choice_value in allowed_statuses
        ]


