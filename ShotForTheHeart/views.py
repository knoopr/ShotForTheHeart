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

from django.contrib.auth import logout as Logout #wanted to keep naming convention for view functions
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.template.loader import get_template
from django.template.context_processors import csrf
from datetime import datetime
import ShotForTheHeart.models as models
from PIL import Image
import base64
from re import match


def main(request):
	template = get_template('main.html')
	html = template.render(RequestContext(request, {'city': 'Guelph', 'active_tab': 'Home'}))
	return HttpResponse(html)


def fundraising(request):
	template = get_template('fundraising.html')
	html = template.render(RequestContext(request, {'city': 'Guelph', 'active_tab': 'Fundraising'}))
	return HttpResponse(html)



@login_required
def profile(request):
	if request.method == 'GET':
		request.user.updateTime()
		template = get_template('profile.html')
		user_caught = request.user.user_eliminated
		user_active = request.user.is_active
		html = template.render(RequestContext(request, {'city': 'Guelph', 'active_tab': 'Profile', 'caught' : user_caught, 'active': user_active}))
		return HttpResponse(html)
	if request.method == 'POST':
		if 'Caught' in request.POST:
			if request.user.user_eliminated:
				if request.POST.get('Caught') == 'True':
					request.user.is_active = False
					request.user.save()
				else:
					request.user.user_eliminated = False
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
			html = template.render(RequestContext(request, {'city': 'Guelph', 'active_tab': 'Login', 'success_message':'You were registered succesfully, please follow the link in your email.'}))
		else:
			html = template.render(RequestContext(request, {'city': 'Guelph', 'active_tab': 'Login'}))
		return HttpResponse(html)
	elif request.method == 'POST':
		result = models.authorize(request)
		if 'ERROR' in result:
			dict = {'city': 'Guelph', 'active_tab': 'Login', 'error_message':'Please enter a valid email and password!'}
			email = request.POST.get('Email')
			dict['email_field'] = 'value=%s' %(email)
			dict['pass_field'] = 'autofocus=""'
			template = get_template('login.html')
			dict.update(csrf(request))
			html = template.render(dict)
			return HttpResponse(html)
		else:
			return HttpResponseRedirect('/profile/')

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
		html = template.render(RequestContext(request, {'city': 'Guelph', 'active_tab': 'Login', 'display':'none'}))
		return HttpResponse(html)
	elif request.method == 'POST':
		result = models.register(request)
		if 'ERROR' in result:
			dict = {'city': 'Guelph', 'active_tab': 'Login', 'display':'block', 'message':result['ERROR']}
			email = request.POST.get('Email')
			dict['email_field'] = 'value=%s' %(email)
			dict['pass_field'] = 'autofocus=""'
			template = get_template('register.html')
			dict.update(csrf(request))
			html = template.render(dict)
			return HttpResponse(html)
		else:
			return HttpResponseRedirect('/login/?last=/register/')
		
@login_required
def target(request):
	if request.method == 'GET':
		target_User = models.CustomUser.objects.get(id=request.user.target_id)
		template = get_template('target.html')
		target = {'picture' : target_User.profile_photo, 'name':target_User.full_name, 'program' : target_User.study_program, 'year': target_User.study_year, 'location' : target_User.hangout_spot, 'caught' : target_User.user_eliminated}
		html = template.render(RequestContext(request,{'city': 'Guelph', 'active_tab': 'Target', 'target' : target}))
		return HttpResponse(html)
	if request.method == 'POST':
		target_User = models.CustomUser.objects.get(id=request.user.target_id)
		target_User.user_eliminated = True
		target_User.save()
		return HttpResponseRedirect("/target")


def upload(request):
	if request.method == 'POST':
		processor = models.ImageProcessor(request)
		processor.CropImage()
		return HttpResponse(processor.SaveImage(request.user))
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
			return HttpResponse('It works! Your email is: ' + New_user.user_email)
		except Exception as e:
			raise Http404('You appear to have been directed to this page in error, or a link has expired')
	else:
		raise Http404('You appear to have been directed to this page in error')