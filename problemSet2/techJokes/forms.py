from urllib.parse import urlparse

from django import forms
from django.core.exceptions import ValidationError

from .models import Joke

APPROVED_IMPORT_HOST = 'web05.cs.ait.ac.th'

class JokeForm(forms.ModelForm):
    existing_category = forms.ChoiceField(
        required=False,
        label='Category',
        choices=[('', '---------')],
    )
    new_category = forms.CharField(
        required=False,
        label='New category',
        max_length=100,
    )

    class Meta:
        model = Joke
        fields = ['text', 'author']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = (
            Joke.objects.exclude(category='')
            .values_list('category', flat=True)
            .distinct()
            .order_by('category')
        )
        self.fields['existing_category'].choices = [('', '---------')] + [
            (category, category) for category in categories
        ]

    def clean_text(self):
        text = self.cleaned_data.get('text', '')
        if not text or not text.strip():
            raise ValidationError('Joke text cannot be empty.')
        return text.strip()

    def clean_author(self):
        author = self.cleaned_data.get('author', '')
        if not author or not author.strip():
            raise ValidationError('Author cannot be empty.')
        return author.strip()

    def clean(self):
        cleaned_data = super().clean()
        existing_category = cleaned_data.get('existing_category', '')
        new_category = cleaned_data.get('new_category', '').strip()

        if existing_category and new_category:
            raise ValidationError(
                'Provide either an existing category or a new category, not both.'
            )

        if new_category:
            cleaned_data['category'] = new_category
        elif existing_category:
            cleaned_data['category'] = existing_category
        else:
            cleaned_data['category'] = ''

        return cleaned_data

    def save(self, commit=True):
        joke = super().save(commit=False)
        joke.category = self.cleaned_data.get('category', '')
        if commit:
            joke.save()
        return joke

class ImportJokesForm(forms.Form):
    xml_url = forms.URLField(label='XML export URL')

    def clean_xml_url(self):
        url = self.cleaned_data['xml_url']
        parsed = urlparse(url)

        if parsed.scheme not in ('http', 'https'):
            raise ValidationError('Only http:// and https:// URLs are allowed.')

        if parsed.hostname != APPROVED_IMPORT_HOST:
            raise ValidationError(
                f'Imports are only allowed from {APPROVED_IMPORT_HOST}.'
            )

        return url
