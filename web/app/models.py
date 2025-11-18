from django.db import models
from django.contrib.auth.models import User

class Cocks(models.Model):
    id = models.AutoField(primary_key=True)
    bloodline = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    location = models.CharField(max_length=120)
    image1 = models.ImageField(upload_to='images/')
    image2 = models.ImageField(upload_to='images/')
    image3 = models.ImageField(upload_to='images/')
    broodcock = models.ImageField(upload_to='images/')
    broodhen = models.ImageField(upload_to='images/')
    comment = models.CharField(max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    liked = models.IntegerField(default=0)
    is_sold = models.BooleanField(default=False)

    def __strt__(self):
        return self.owner

