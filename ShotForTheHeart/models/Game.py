from django.db import models
from django.conf import settings
from datetime import datetime

class Game (models.Model):
	game_location = models.CharField(max_length=50, blank=True)
	fundraising_link = models.CharField(max_length=127, blank=True)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	users_needing_target = models.ManyToManyField(settings.AUTH_USER_MODEL)
	game_started = models.BooleanField(default=True)
	
	def __str__ (self):
		return self.game_location
	
	
	#if the user is targeting themselves add them to the wait list
	#Each player should only be targeted by one person (for game fairness) and should only have one target
	#If there is a player waiting for a target (as they somehow targeted themselves) they will take over the target of a player who just captured
	#It should never reach this stage theoretically
	def getTarget(self, requsting_user):
		if requesting_user.target.target == requesting_user:
			self.users_needing_target.add(requesting_user)
			requesting_user.target = None
			requesting_user.save()
		elif self.users_needing_target.count > 0:
			waiting_user = self.users_needing_target.all()[0]
			if waiting_user != requesting_user.target.target:
				waiting_user.target = requesting_user.target.target
				waiting_user.save()
				self.users_needing_target.add(requesting_user)
				requesting_user.target = None
				requesting_user.save()
		else:
			requesting_user.target = requesting_user.target.target
			requesting_user.save()
		
		self.save()
				
	def gameStarted(self):
		if self.game_started:
			return True
		elif self.start_date is None:
			return False
		elif self.start_date > datetime.now():
			return False
		
		#Otherwise the game has started but initial targets haven't been set
		else:
			all_Players = settings.AUTH_USER_MODEL.objects.all().filter(is_staff=False).exclude(full_name__exact='').exclude(study_program__exact='').exclude(hangout_spot__exact='').exclude(profile_photo__exact='')
			player_count = len(all_Players)
			for index, player in enumerate(all_players):
				player.target = all_players[(index+1)%player_count]
				player.save()
			
			self.game_started = True
			self.save()
			
			return True
			
			
				
		
		
		
	