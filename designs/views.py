from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,EditProfileForm,DesignsForm
from django.contrib.auth.models import User
from .models import Profile,Designs
from django.core.urlresolvers import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required





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








