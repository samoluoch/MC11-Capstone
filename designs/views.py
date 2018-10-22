from django.shortcuts import render

# Create your views here.
def home(request):
    # posts = Post.objects.all()

    return render(request,'home.html')