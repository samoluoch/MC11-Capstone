from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,EditProfileForm
from django.contrib.auth.models import User
from .models import Profile




# Create your views here.
def home(request):
    # posts = Post.objects.all()

    return render(request,'home.html')

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


def profile(request,username):
    profile = User.objects.get(username=username)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    posts = Post.get_profile_posts(profile.id)
    title = f'@{profile.username} Projects'


    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'posts':posts, 'profile_details':profile_details})



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














