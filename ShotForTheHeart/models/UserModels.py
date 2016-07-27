from datetime import datetime
from decimal import Decimal
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login, get_user_model
from .Game import Game
import hashlib
import re



class UserManager (BaseUserManager):
	def create_user(self,email,password=None):
		try:
			user = self.model(user_email = email)
			user.set_password(password)
			email_hash = hashlib.sha256(email)
			user.set_url(email_hash.hexdigest())
			user.save()
			return {'VALID': user}
		except:
			return {'ERROR': 'A user with that email already exists!'}
	
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
	study_year = models.PositiveSmallIntegerField(default=0)
	hangout_spot = models.CharField(max_length=50, blank=True)
	profile_photo = models.ImageField(upload_to='./', blank=True)
	#last_login = models.DateTimeField(null=True, blank=True)
	user_eliminated = models.SmallIntegerField(default=0)
	target_id = models.PositiveSmallIntegerField(null=True, blank=True)
	money_raised = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal(0.00))
	activation_url = models.CharField(max_length=126, blank=True)
	participating_game = models.ForeignKey(Game, on_delete=models.PROTECT, default=1)
	
	#Required Fields
	is_staff = models.BooleanField(_('staff status'), default=False, help_text = ("Designates whether the user can login to the admin site"))
	is_active = models.BooleanField(_('active'), default=False, help_text = ("Whether the user is active or not, set to false instead of deleting accounts"))
	date_joined = models.DateTimeField(_("Date joined"), default=timezone.now)


	USERNAME_FIELD = 'user_email'
	objects = UserManager()
	
	def set_url(self, email_hash):
		self.activation_url = email_hash
		self.save()
	
	def get_full_name(self):
		return self.full_name
	
	def get_short_name(self):
		return self.full_name
		
	def updateTime(self):
		self.last_login = datetime.now()
		self.save(update_fields=['last_login'])
		
	def updateInfo(self, POST):
		self.full_name = POST.get('full_name')
		self.study_program = POST.get('study_program')
		self.study_year = POST.get('study_year')
		self.hangout_spot = POST.get('hangout_spot')
		self.save()
	
	def getTarget(self):
		target_user = CustomUser.objects.get(id=self.target_id)
		while target_user.user_eliminated == 2:
			self.target_id = target_user.target_id
			self.save()
			target_user = CustomUser.objects.get(id=self.target_id)
		return target_user