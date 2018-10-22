from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save,sender=User)
def create_profile(sender, instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender, instance,**kwargs):
    instance.profile.save()

# Create your models here.
class Profile(models.Model):
    photo = models.ImageField(upload_to='image/', null=True)
    email = models.CharField(max_length =30, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=1)



    def __str__(self):
        return self.user.username

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.save()

    class Meta:
        ordering = ['email']

    @classmethod
    def search_profile(cls, name):
        profile = Profile.objects.filter(user__username__icontains=name)
        return profile

    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user=id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user=id).first()
        return profile


class Designs(models.Model):
    '''
    This is post class model
    '''
    title = models.CharField(max_length =60)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(User, null=True)
    comment = models.TextField(null=True)
    file = models.FileField(upload_to='files/', null=True)




    def save_post(self):
        self.save()

    def delete_image(self):
        self.delete()



    @classmethod
    def get_profile_designs(cls, profile):
        designs = Designs.objects.filter(profile__id=profile)
        return designs

    @classmethod
    def get_location_designs(cls, location):
        designs = Designs.objects.filter(location__id=location)
        return designs

    @classmethod
    def search_by_category(cls, search_term):
        designs = cls.objects.filter(category__name__icontains=search_term)
        return designs

    @classmethod
    def search_by_location(cls, search_term):
        designs = cls.objects.filter(location__name__icontains=search_term)
        return designs


    @classmethod
    def all_posts(cls):
        designs = cls.objects.all()
        return designs























