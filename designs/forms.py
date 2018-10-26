from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Designs
from django.utils.translation import ugettext_lazy as _



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text = 'Required')

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1', 'password2')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class DesignsForm(forms.ModelForm):
    class Meta:
        model = Designs
        exclude = ['pub_date', 'profile', 'cost', 'product']

# #Braintree payment forms
# class CheckoutForm(forms.Form):
#     payment_method_nonce = forms.CharField(
#         max_length=1000,
#         widget=forms.widgets.HiddenInput,
#         require=False,  # In the end it's a required field, but I wanted to provide a custom exception message
#     )
#
#     def clean(self):
#         self.cleaned_data = super(CheckoutForm, self).clean()
#         # Braintree nonce is missing
#         if not self.cleaned_data.get('payment_method_nonce'):
#             raise forms.ValidationError(_(
#                 'We couldn\'t verify your payment. Please try again.'))
#         return self.cleaned_data

