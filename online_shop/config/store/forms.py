from django import forms
from .bulma_mixin import BulmaMixin
from .models import Order
from .models import Review, RATE_CHOICES


class OrderForm(BulmaMixin, forms.Form):
    address = forms.CharField(label='Address or Phone Number')

    class Meta:
        model = Order
        fields = ['address']


class RateForm(forms.ModelForm, BulmaMixin):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), label='Leave your review here')
    rate = forms.ChoiceField(choices=RATE_CHOICES, required=True, label='Rate product from 1 to 5')

    class Meta:
        model = Review
        fields = ('text', 'rate')