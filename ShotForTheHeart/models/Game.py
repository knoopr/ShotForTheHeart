from django.db import models
from .UserModels import CustomUser

class UserManager (BaseUserManager):
	game_location = models.CharField(max_length=50, blank=True)
	fundraising_link = models.CharField(max_length=127, blank=True)
	start_date = models.datefield(blank=True)
	end_date = models.datefield(blank=True)
	users_needing_target = models.ManyToManyField(CustomUser)
	
	
	