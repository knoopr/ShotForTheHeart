from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from hashlib import md5
from io import BytesIO
from PIL import Image
import base64
import re


class UserManager (BaseUserManager):
	def create_user(self,email,password=None):
		user = self.model(user_email = email)
		user.set_password(password)
		user.save()
		return user
	
	def create_superuser(self,email,password):
		user=self.create_user(email,password)
		user.is_staff = True
		user.save()
		return user()

class CustomUser(AbstractBaseUser):
	class Meta:
		app_label = 'ShotForTheHeart'
		verbose_name = 'user'
		verbose_name_plural = 'users'
	
	
	user_email = models.CharField(max_length=127, unique=True, validators=[
		validators.RegexValidator(
			re.compile("[a-zA-Z0-9_\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+"),
			_("Enter a valid email."),
			"ERROR")
			])
	full_name = models.CharField(max_length=126, blank=True)
	study_program = models.CharField(max_length=50, blank=True)
	study_year = models.PositiveSmallIntegerField(null=True, blank=True)
	hangout_spot = models.CharField(max_length=50, blank=True)
	profile_photo = models.ImageField(upload_to='./', blank=True)
	#last_login = models.DateTimeField(null=True, blank=True)
	user_eliminated = models.BooleanField(default=False)
	target_id = models.PositiveSmallIntegerField(null=True, blank=True)
	
	#Required Fields
	is_staff = models.BooleanField(_('staff status'), default=False, help_text = ("Designates whether the user can login to the admin site"))
	is_active = models.BooleanField(_('active'), default=False, help_text = ("Whether the user is active or not, set to false instead of deleting accounts"))
	date_joined = models.DateTimeField(_("Date joined"), default=timezone.now)


	USERNAME_FIELD = 'user_email'
	objects = UserManager()
	
	def get_full_name(self):
		return self.full_name
	
	def get_short_name(self):
		return self.full_name
	
	def ChangeProgram(self, program_post):
		if len(program_post) < 50:
			self.study_program = program_post
			self.save()
			return True
		return False
			
	def ChangeYear(self, year_post):
		if year_post is not None and year_post.isdigit():
			self.study_year = int(year_post)
			self.save()
			return True
		return False
	
	def ChangeHangout(self, hangout_post):
		if len(hangout_post) < 50:
			self.study_hangout = hanout_post
			self.save()
			return True
		return False
		
	
	

def authorize(request):
	email = request.POST.get('Email')
	password = request.POST.get('Password')
	if len(email) < 6 or len(password) < 10:
		return {'ERROR' : 'Too short'}
	else:
		user = authenticate(username = email, password = password)
		if user is not None:
			login(request,user)
			return {'VALID' : 'Logged in succesfully'}
		else:
			return {'ERROR' : 'Username or password incorrect'}
		
def register(request):
	email = request.POST.get('Email')
	password = request.POST.get('Password')
	confirm = request.POST.get('confirmPassword')
	if password != confirm:
		return {'ERROR' : 'Unmatched Passwords'}
	else:
		user = CustomUser.objects.create_user(email=email, password=password)
		return {'VALID' : 'GOOD'}
	
		
def CropImage(request):
	img64 = request.POST.get('imgUrl')
	img64 = img64[img64.find(',')+1:]
	img = Image.open(BytesIO(base64.b64decode(img64)))
	img.save("/var/www/html/ShotForTheHeart/media/tmp/" + md5(img.tobytes()).hexdigest()+ ".jpg")
	return img64