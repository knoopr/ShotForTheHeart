# Copyright (C) 2015 Rick Knoop

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
import base64
from django.contrib.auth import logout as Logout #wanted to keep naming convention for view functions
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404,  HttpResponseBadRequest
from django.template import RequestContext
from django.template.loader import get_template
from django.template.context_processors import csrf
from datetime import datetime
from hashlib import md5
from PIL import Image
from re import match
import ShotForTheHeart.models as models
import ShotForTheHeart.utils as utils



@login_required
def adminUsers(request):
	if request.user.is_staff:
		if request.method == 'GET':
			template = get_template('admin.html')
			active_users = models.CustomUser.objects.filter(is_active=True).exclude(user_eliminated=-1)
			eliminated_users = models.CustomUser.objects.filter(user_eliminated=2)
			inactive_users = models.CustomUser.objects.filter(is_active=False).exclude(user_eliminated=2)
			html = template.render(RequestContext(request, {'city': 'USERS', 'Active': active_users, 'Inactive' : inactive_users, 'Eliminated' : eliminated_users}))
			return HttpResponse(html)
		else:
			return HttpResponseBadRequest()
	else:
		return HttpResponseRedirect('/profile/')



@login_required
def adminContests(request):
	if request.user.is_staff:
		if request.method == 'GET':
			template = get_template('admin.html')
			users_contesting = models.CustomUser.objects.filter(user_eliminated=-1)
			contested_users = []
			for user in users_contesting:
				Captor = models.CustomUser.objects.get(target_id=user.id, is_active=True)
				contested_users.append({'Captor':Captor,'Captive': user})
			html = template.render(RequestContext(request, {'city': 'CAPTURE', 'Contested': contested_users}))
			return HttpResponse(html)
		else:
			users_contesting = models.CustomUser.objects.filter(user_eliminated=-1)
			for captive_user in users_contesting:
				contest_decision = request.POST.get(str(captive_user.id))
				if contest_decision == "Captor":
					captive_user.user_eliminated = 2
					captive_user.is_active = False
					captive_user.save()
				else:
					captive_user.user_eliminated = 1
					captive_user.is_active = True
					captive_user.save()
			return HttpResponseRedirect("/admin/")
	else:
		return HttpResponseRedirect('/profile/')



def main(request):
	template = get_template('main.html')
	html = template.render(RequestContext(request, {'city': 'Guelph'}))
	return HttpResponse(html)



def fundraising(request):
	template = get_template('fundraising.html')
	html = template.render(RequestContext(request, {'city': 'Guelph'}))
	return HttpResponse(html)



@login_required
def profile(request):
	if request.method == 'GET':
		request.user.updateTime()
		template = get_template('profile.html')
		user_caught = request.user.user_eliminated
		user_active = request.user.is_active
		html = template.render(RequestContext(request, {'city': request.user.participating_game, 'caught' : user_caught, 'active': user_active}))
		return HttpResponse(html)
	if request.method == 'POST':
		if 'Caught' in request.POST:
			if request.user.user_eliminated == 1:
				if request.POST.get('Caught') == 'True':
					request.user.user_eliminated = 2
					request.user.is_active = False
					request.user.save()
				else:
					request.user.user_eliminated = -1
					request.user.save()
				return HttpResponseRedirect('/profile')
			else:
				return HttpResponseForbidden()
		else:
			request.user.updateInfo(request.POST)
			return HttpResponseRedirect('/profile')
			

	
def login(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			return HttpResponseRedirect('/profile/')
		template = get_template('login.html')
		if request.GET.get('last') == '/register/':
			html = template.render(RequestContext(request, {'city': 'Success', 'success_message':'You were registered succesfully, please follow the link in your email.'}))
		if request.GET.get('last') == '/activate/':
			html = template.render(RequestContext(request, {'city': 'Success', 'success_message':'Your account is now active; please login now.'}))
		else:
			html = template.render(RequestContext(request, {'city': 'Guelph'}))
		return HttpResponse(html)
	elif request.method == 'POST':
		result = utils.authorize(request)
		if 'ERROR' in result:
			display_dict = {'city': 'Guelph', 'error_message':'Please enter a valid email and password!'}
			email = request.POST.get('Email')
			display_dict['email_field'] = 'value=%s' %(email)
			display_dict['pass_field'] = 'autofocus=""'
			template = get_template('login.html')
			display_dict.update(csrf(request))
			html = template.render(display_dict)
			return HttpResponse(html)
		else:
			if request.GET.get('next') == None:
				return HttpResponseRedirect('/profile/')
			else:
				return HttpResponseRedirect(request.GET.get('next'))

def logout(request):
	Logout(request)
	return HttpResponseRedirect('/')
	
	
def picture(request):
	response = HttpResponse(content_type = "image/jpeg")
	filename = "/var/www/html/ShotForTheHeart/" + request.path_info
	img = Image.open(filename)
	img.save(response,"JPEG")
	return response

	
def register(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			return HttpResponseRedirect('/profile/')
		template = get_template('register.html')
		html = template.render(RequestContext(request, {'city': 'Guelph', 'display':'none'}))
		return HttpResponse(html)
	elif request.method == 'POST':
		result = utils.register(request)
		if 'ERROR' in result:
			display_dict = {'city': 'Guelph', 'display':'block', 'message':result['ERROR']}
			email = request.POST.get('Email')
			display_dict['email_field'] = 'value=%s' %(email)
			display_dict['pass_field'] = 'autofocus=""'
			template = get_template('register.html')
			display_dict.update(csrf(request))
			html = template.render(display_dict)
			return HttpResponse(html)
		else:
			return HttpResponseRedirect('/login/?last=/register/')
		
@login_required
def target(request):
	if request.method == 'GET':
		player_caught = True if request.user.user_eliminated == 2 else False
		if request.user.participating_game.start_date is None:
			game_started = False
		elif request.user.participating_game.start_date < datetime.now():
			game_started = False
		else:
			game_started = True
		template = get_template('target.html')
		html = template.render(RequestContext(request,{'city': 'Guelph', 'caught': player_caught, "started" : game_started}))
		return HttpResponse(html)
	if request.method == 'POST':
		request.user.target.user_eliminated = 1
		request.user.target.save()
		return HttpResponseRedirect("/target")


def upload(request):
	if request.method == 'POST':
		processor = models.ImageProcessor(request)
		processor.CropImage()
		filename = md5(request.user.user_email).hexdigest()+ ".jpg"
		save_result = processor.SaveImage(filename)
		if save_result:
			request.user.profile_photo = filename
			request.user.save()
			return HttpResponse('''{
				"status" : "success",
				"url" : "/media/%s"
				}''' % filename)
		else:
			return HttpResponse('''{
				"status" : "error",
				"message" : "There was an error uploading the file"
				}''')
	else:
		return HttpResponse(status=405)
	

def base(request):
	template = get_template('base.html')
	html = template.render({'city': 'Guelph'})
	return HttpResponse(html)

def activate(request):
	strMatch = match('\/register\/(.*)$', request.path)
	if strMatch and '/' not in strMatch.group(1):
		try:
			New_user = models.CustomUser.objects.get(activation_url=strMatch.group(1))
			New_user.activation_url = ""
			New_user.is_active = True
			New_user.save()
			return HttpResponseRedirect('/login/?last=/activate/')
		except Exception as e:
			raise Http404('You appear to have been directed to this page in error, or a link has expired')
	else:
		raise Http404('You appear to have been directed to this page in error')
