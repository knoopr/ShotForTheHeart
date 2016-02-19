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
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.template.context_processors import csrf
from datetime import datetime
import ShotForTheHeart.models as models
from PIL import Image
import base64


def main(request):
	template = get_template('main.html')
	html = template.render(RequestContext(request, {'city': 'Guelph', 'active_tab': 'home'}))
	#request.session['hello'] = 'apple'
	'''response = HttpResponse(html)
	response.set_cookie('last_visit', datetime.datetime.now(), httponly=True)
	return response'''
	return HttpResponse(html)


@login_required
def profile(request):
	request.user.updateTime()
	template = get_template('profile.html')
	html = template.render(RequestContext(request, {'city': 'Guelph', 'active_tab': 'profile'}))
	return HttpResponse(html);

	
def login(request):
	# if request.method == 'GET':
	# 	template = get_template('login.html')
	# 	html = template.render({'city': 'Guelph', 'active_tab': 'login'})
	# 	return HttpResponse(html);
	# elif request.method == 'POST':
	# 	return HttpResponse("Posted succesfully")
	if request.method == 'GET':
		template = get_template('login.html')
		html = template.render(RequestContext(request, {'city': 'Guelph', 'active_tab': 'login', 'display':'none'}))
		return HttpResponse(html);
	elif request.method == 'POST':
		result = models.authorize(request)
		#template = get_template('profile.html')
		#return HttpResponse(template.render({'city':'Guelph', 'active_tab': 'profile'}))
		if 'ERROR' in result:
			dict = {'city': 'Guelph', 'active_tab': 'login', 'display':'block', 'message':'Please enter a valid email and password!'}
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
		template = get_template('register.html')
		html = template.render(RequestContext(request, {'city': 'Guelph', 'active_tab': 'login', 'display':'none'}))
		return HttpResponse(html);
	elif request.method == 'POST':
		result = models.register(request)
		if 'ERROR' in result:
			dict = {'city': 'Guelph', 'active_tab': 'login', 'display':'block', 'message':'Please enter a valid email and password!'}
			email = request.POST.get('Email')
			dict['email_field'] = 'value=%s' %(email)
			dict['pass_field'] = 'autofocus=""'
			template = get_template('register.html')
			dict.update(csrf(request))
			html = template.render(dict)
			return HttpResponse(html)
		else:
			return profile(request)
		

def target(request):
	template = get_template('target.html')
	target = {'picture' : 'http://i.imgur.com/VBQgNPm.jpg', 'name':'Billy Generic', 'program' : 'Business', 'year': '5th', 'location' : 'Johnston'}
	html = template.render(RequestContext(request,{'city': 'Guelph', 'active_tab': 'target', 'target' : target}))
	return HttpResponse(html);


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
	return HttpResponse(html);

