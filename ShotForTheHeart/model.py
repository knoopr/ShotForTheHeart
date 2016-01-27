from django.core import validators
from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import re


class UserManager (BaseUserManager):
	def create_user(self,email,password=None):
		user = self.model(email)
		user.set_password(password)
		user.save()
		return user
	
	def create_superuser(self,email,password):
		user=self.create_user(email,password)
		user.is_staff = True
		user.save()
		return user()



'''class userInfo (models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	study_program = models.CharField(max_length=50)
	study_year = models.PositiveSmallIntegerField()
	hangout_spot = models.CharField(max_length=50)
	profile_photo = models.ImageField(upload_to='tmp')

	def ChangeProgram(program_post):
		if len(program_post) < 50:
			self.study_program = program_post
			self.save()
			return True
		return False
			
	def ChangeYear(year_post):
		if year_post is not None and year_post.isdigit():
			self.study_year = int(year_post)
			self.save()
			return True
		return False
	
	def ChangeHangout(hangout_post):
		if len(hangout_post) < 50:
			self.study_hangout = hanout_post
			self.save()
			return True
		return False
		
'''
class CustomUser(AbstractBaseUser):
	
	class Meta:
		app_label = 'ShotForTheHeart'
		db_table = 'Users'
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
	study_year = models.PositiveSmallIntegerField(blank=True)
	hangout_spot = models.CharField(max_length=50, blank=True)
	profile_photo = models.ImageField(upload_to='tmp', blank=True)
	#last_login = models.DateTimeField(null=True, blank=True)
	user_eliminated = models.BooleanField(default = False)
	target_id = models.PositiveSmallIntegerField(blank=True)
	
	#Required Fields
	is_staff = models.BooleanField(_('staff status'), default=False, help_text = ("Designates whether the user can login to the admin site"))
	is_active = models.BooleanField(_('active'), default=True, help_text = ("Whether the user is active or not, set to false instead of deleting accounts"))
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