from django.db import models
from django.contrib.auth.models import User
from re import search as regex



class userInfo (models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	program = models.CharField(max_length=50)
	year = models.CharField(max_length=3)
	hangout = models.CharField(max_length=50)
	profile_photo = models.ImageField(upload_to='tmp')

def authorize(request):
	email = request.POST.get('Email')
	password = request.POST.get('Password')
	if len(email) < 6 or len(password) < 8:
		return {'ERROR' : 'Too short'}
		
def register(request):
	email = request.POST.get('Email')
	password = request.POST.get('Password')
	confirm = request.POST.get('confirmPassword')
	if password != confirm:
		return {'ERROR' : 'Unmatched Passwords'}
	elif regex("[a-zA-Z0-9_\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+", email) is None:
		return {'ERROR' : 'Invalid Email'}
	else:
		return {'VALID' : 'GOOD'}