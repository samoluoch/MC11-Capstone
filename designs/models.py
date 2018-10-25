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
    title = models.CharField(max_length =150)
    details = models.TextField()
    number_of_bedrooms = models.IntegerField(max_length =60)
    bedrooms_size = models.IntegerField(max_length =60)
    number_of_washrooms = models.IntegerField(max_length =60)
    washroom_size = models.IntegerField(max_length =60)
    total_size = models.IntegerField(max_length =60)
    pub_date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(User, null=True)
    profile = models.ForeignKey(User)
    cost = models.IntegerField(max_length =60, null=True)
    house_type = models.CharField(max_length =150, null=True)
    land_location = models.CharField(max_length =150, null=True)
    date_of_completion = models.DateField(null=True)
    floor_area = models.IntegerField(max_length =60, null=True)
    number_of_bedrooms = models.IntegerField(max_length =60, null=True)
    number_of_washrooms = models.IntegerField(max_length =60, null=True)
    washroom_size = models.IntegerField(max_length =60, null=True)
    living_room_size = models.IntegerField(max_length =60, null=True)
    master_bedroom_size = models.IntegerField(max_length =60, null=True)
    bedrooms_size = models.IntegerField(max_length =60, null=True)
    kitchen_size = models.IntegerField(max_length =60, null=True)
    number_of_windows = models.IntegerField(max_length =60, null=True)
    wall_material = models.TextField(null=True)
    ventilation_description = models.TextField(null=True)
    roofing_description = models.TextField(null=True)
    file_1 = models.FileField(upload_to='files/', blank=True)
    file_2 = models.FileField(upload_to='files/', blank=True)
    file_3 = models.FileField(upload_to='files/', blank=True)
    file_4 = models.FileField(upload_to='files/', blank=True)
    file_5 = models.FileField(upload_to='files/', blank=True)
    product = models.FileField(upload_to='files/', default='Will be uploaded')



    def save_design(self):
        self.save()

    def delete_design(self):
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























