from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Creating User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 100, blank = True)
    last_name = models.CharField(max_length = 100, blank = True)
    email = models.CharField(max_length = 100, blank = True)
    image = models.ImageField(default = 'default.png', upload_to = 'profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

# Creating receiver that will automatically create a new profile for each user registered
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
