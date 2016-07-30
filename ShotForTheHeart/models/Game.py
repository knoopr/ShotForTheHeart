from django.db import models
from django.conf import settings


class Game (models.Model):
	game_location = models.CharField(max_length=50, blank=True)
	fundraising_link = models.CharField(max_length=127, blank=True)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	users_needing_target = models.ManyToManyField(settings.AUTH_USER_MODEL)
	
	def __str__ (self):
		return self.game_location
	
	def get_target(self):
		
		
		
	