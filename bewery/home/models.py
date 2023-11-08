from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
r_choice = ( 
    ("1", "1"), 
    ("2", "2"), 
    ("3", "3"), 
    ("4", "4"), 
    ("5", "5")
) 
class Review(models.Model):
    brew_id = models.TextField(default="No Id")
    comment = models.TextField()
    rating = models.CharField(max_length=10, choices=r_choice,default=1)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment