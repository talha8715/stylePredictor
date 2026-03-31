from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class uimage(models.Model):
    caption=models.CharField(max_length=100)
    image=models.ImageField(upload_to="img/%y")
    def __str__(self):
        return self.caption

#.......................................................................

class userd(models.Model):
	uid = models.IntegerField(blank=False, null=False)	
	name=models.CharField(max_length=20, default = '')

	def __str__(self):
		return self.name

#.......................................................................

class UserModal(models.Model):
    area = (
        ('U', 'Urban'),
        ('R', 'Rural'),
        
    )
    

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    area = models.CharField(max_length=20, choices=area, default='')
    city = models.CharField(max_length=100,  default='')
    occupation = (
        ('S', 'Student'),
        ('T', 'Teacher'),
        ('B', 'Businessman'),
        ('D', 'Doctor'),
        ('E', 'Engineer'),
 
    )
    gender = (
        ('M', 'Male'),
        ('F', 'Female'),
        
    )
    education = (
        ('M', 'Matriculation'),
        ('I', 'Intermediate'),
        ('B', 'Bachelor_Degree'),
        ('MS', 'Master_Degree')
    )
    occupation = models.CharField(max_length=20, choices=occupation, default='')
    gender = models.CharField(max_length=20, choices=gender, default='')
    age = models.IntegerField(blank=True, null=True,  default='')
    education = models.CharField(max_length=20, choices=education, default='')

    def __str__(self):
        return self.user

#.......................................................................

class FashionModel(models.Model):
    fav_color = (
        ('B', 'black'),
        ('R', 'red'),
        ('W', 'white'),
        ('G', 'green'),
        
    )

    name = models.CharField(max_length=30, blank= False, null =False, default='')
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fashion_consious = models.CharField(max_length=20, default='')
    brand_consious = models.CharField(max_length=20, default='')
    fav_color = models.CharField(max_length=20, choices=fav_color, default='')
    fav_dressing_type = (
        ('F', 'formal'),
        ('C', 'casual'),
        ('SF', 'semi_formal')
        
    )
    
    fav_design = (
        ('CK', 'check'),
        ('P', 'plain'),
        ('L', 'lines')
      
    )
    fav_dressing_type = models.CharField(max_length=20, choices=fav_dressing_type, default='')
    fav_design = models.CharField(max_length=20, choices=fav_design, default='')

    def __str__(self):
        return self.name

#.......................................................................

class PlanModel(models.Model):

    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank= False, null =False, default='')
    content = models.TextField(blank=True)
    event = (
        ('S', 'social'),
        ('R', 'Religious'),
        ('I', 'islamic'),
        
    )
    event= models.CharField(max_length=20, choices=event, default='')
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
    time = models.TimeField()
    priority = (
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
      
    )
    priority = models.CharField(max_length=20, choices=priority, default='')

    class Meta:
        ordering = ["-created"] #ordering by the created field

    def __str__(self):
        return self.title

#.......................................................................

