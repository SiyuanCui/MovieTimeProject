from django import forms
from reviewapp.models import Review, CommentOnReview


class RateForm(forms.ModelForm):
	stars = forms.IntegerField(min_value=1, max_value=10)
	text = forms.CharField(widget=forms.Textarea, required=False)
	class Meta:
		model = Review
		fields = ('stars', 'text')


class CommentForm(forms.ModelForm):
	body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
	class Meta:
		model = CommentOnReview
		fields = ('body',)