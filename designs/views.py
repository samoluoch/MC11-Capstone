from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,EditProfileForm,DesignsForm
from django.contrib.auth.models import User
from .models import Profile,Designs
from django.core.urlresolvers import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received


# #Braintree importations
# import braintree
#
# from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from django.utils.decorators import method_decorator
# from django.views import generic
#
# from . import forms



# Create your views here.
def home(request):
    # form=DesignForm()
    designs = Designs.objects.all()
    return render(request,'home.html',{"designs":designs})

@login_required(login_url='/login')
def orders(request):
    # form=DesignForm()
    designs = Designs.objects.all()
    return render(request,'orders.html',{"designs":designs})

@login_required(login_url='/login')
def order_detail(request,id):
    # form=DesignForm()
    designs = Designs.objects.get(id=id)
    return render(request,'order_details.html',{"designs":designs})

# def home(request):
#     # posts = Post.objects.all()
#
#     return render(request,'home.html')

def register(request):
    if request.user.is_authenticated():
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # user.is_active = False
                user.save()
                # current_site = get_current_site(request)
                # to_email = form.cleaned_data.get('email')
                # activation_email(user, current_site, to_email)
                # return HttpResponse('Please confirm your email')
            return redirect('auth_login.html')

        else:
            form = RegistrationForm()
        return render(request, 'registration/signup.html',{'form':form})

@login_required(login_url='/login')
def profile(request,username):
    profile = User.objects.get(username=username)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    designs = Designs.get_profile_designs(profile.id)
    title = f'@{profile.username} Designs'


    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'designs':designs, 'profile_details':profile_details})


@login_required(login_url='/login')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('profile',username=request.user)
    else:
        form = EditProfileForm()

    return render(request, 'profile/edit_profile.html', {'form':form})

@login_required(login_url='/login')
def upload_designs(request):
    if request.method == 'POST':
        form = DesignsForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.profile = request.user
            upload.save()
            return redirect('profile',username=request.user)
    else:
        form = DesignsForm()

    return render(request, 'profile/upload_designs.html', {'form': form})


@login_required(login_url='/login')
def paypal(request):

    paypal_dict = {
        "business": "samoluoch.codes@gmail.com",
        "amount": "999999.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('your-return-view')),
        "cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Creating the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)


# def paypal(sender, **kwargs):
#     ipn_obj = sender
#     if ipn_obj.payment_status == ST_PP_COMPLETED:
#         # WARNING !
#         # Check that the receiver email is the same we previously
#         # set on the `business` field. (The user could tamper with
#         # that fields on the payment form before it goes to PayPal)
#         if ipn_obj.receiver_email != "receiver_email@example.com":
#             # Not a valid payment
#             return
#
#         # ALSO: for the same reason, you need to check the amount
#         # received, `custom` etc. are all what you expect or what
#         # is allowed.
#
#         # Undertake some action depending upon `ipn_obj`.
#         if ipn_obj.custom == "premium_plan":
#             price = ...
#         else:
#             price = ...
#
#         if ipn_obj.mc_gross == price and ipn_obj.mc_currency == 'USD':
#             ...
#     else:
#         #...
#
#         valid_ipn_received.connect(paypal)



# #Braintree views
# class CheckoutView(generic.FormView):
#     """This view lets the user initiate a payment."""
#     form_class = forms.CheckoutForm
#     template_name = 'checkout.html'
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         # We need the user to assign the transaction
#         self.user = request.user
#
#         # Ha! There it is. This allows you to switch the
#         # Braintree environments by changing one setting
#         if settings.BRAINTREE_PRODUCTION:
#             braintree_env = braintree.Environment.Production
#         else:
#             braintree_env = braintree.Environment.Sandbox
#
#         # Configure Braintree
#         braintree.Configuration.configure(
#             braintree_env,
#             merchant_id=settings.BRAINTREE_MERCHANT_ID,
#             public_key=settings.BRAINTREE_PUBLIC_KEY,
#             private_key=settings.BRAINTREE_PRIVATE_KEY,
#         )
#
#         # Generate a client token. We'll send this to the form to
#         # finally generate the payment nonce
#         # You're able to add something like ``{"customer_id": 'foo'}``,
#         # if you've already saved the ID
#         self.braintree_client_token = braintree.ClientToken.generate({})
#         return super(CheckoutView, self).dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         ctx = super(CheckoutView, self).get_context_data(**kwargs)
#         ctx.update({
#             'braintree_client_token': self.braintree_client_token,
#         })
#         return ctx
#
#     def form_valid(self, form):
#         # Braintree customer info
#         # You can, for sure, use several approaches to gather customer infos
#         # For now, we'll simply use the given data of the user instance
#         customer_kwargs = {
#             "first_name": self.user.first_name,
#             "last_name": self.user.last_name,
#             "email": self.user.email,
#         }
#
#         # Create a new Braintree customer
#         # In this example we always create new Braintree users
#         # You can store and re-use Braintree's customer IDs, if you want to
#         result = braintree.Customer.create(customer_kwargs)
#         if not result.is_success:
#             # Ouch, something went wrong here
#             # I recommend to send an error report to all admins
#             # , including ``result.message`` and ``self.user.email``
#
#             context = self.get_context_data()
#             # We re-generate the form and display the relevant braintree error
#             context.update({
#                 'form': self.get_form(self.get_form_class()),
#                 'braintree_error': u'{} {}'.format(
#                     result.message, _('Please get in contact.'))
#             })
#             return self.render_to_response(context)
#
#         # If the customer creation was successful you might want to also
#         # add the customer id to your user profile
#         customer_id = result.customer.id
#
#         """
#         Create a new transaction and submit it.
#         I don't gather the whole address in this example, but I can
#         highly recommend to do that. It will help you to avoid any
#         fraud issues, since some providers require matching addresses
#
#         """
#         address_dict = {
#             "first_name": self.user.first_name,
#             "last_name": self.user.last_name,
#             "street_address": 'street',
#             "extended_address": 'street_2',
#             "locality": 'city',
#             "region": 'state_or_region',
#             "postal_code": 'postal_code',
#             "country_code_alpha2": 'alpha2_country_code',
#             "country_code_alpha3": 'alpha3_country_code',
#             "country_name": 'country',
#             "country_code_numeric": 'numeric_country_code',
#         }
#
#         # You can use the form to calculate a total or add a static total amount
#         # I'll use a static amount in this example
#         result = braintree.Transaction.sale({
#             "customer_id": customer_id,
#             "amount": 100,
#             "payment_method_nonce": form.cleaned_data['payment_method_nonce'],
#             "descriptor": {
#                 # Definitely check out https://developers.braintreepayments.com/reference/general/validation-errors/all/python#descriptor
#                 "name": "COMPANY.*test",
#             },
#             "billing": address_dict,
#             "shipping": address_dict,
#             "options": {
#                 # Use this option to store the customer data, if successful
#                 'store_in_vault_on_success': True,
#                 # Use this option to directly settle the transaction
#                 # If you want to settle the transaction later, use ``False`` and later on
#                 # ``braintree.Transaction.submit_for_settlement("the_transaction_id")``
#                 'submit_for_settlement': True,
#             },
#         })
#         if not result.is_success:
#             # Card could've been declined or whatever
#             # I recommend to send an error report to all admins
#             # , including ``result.message`` and ``self.user.email``
#             context = self.get_context_data()
#             context.update({
#                 'form': self.get_form(self.get_form_class()),
#                 'braintree_error': _(
#                     'Your payment could not be processed. Please check your'
#                     ' input or use another payment method and try again.')
#             })
#             return self.render_to_response(context)
#
#         # Finally there's the transaction ID
#         # You definitely want to send it to your database
#         transaction_id = result.transaction.id
#         # Now you can send out confirmation emails or update your metrics
#         # or do whatever makes you and your customers happy :)
#         return super(CheckoutView, self).form_valid(form)
#
#     def get_success_url(self):
#         # Add your preferred success url
#         return reverse('foo')





