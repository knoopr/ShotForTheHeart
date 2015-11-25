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

from django.http import HttpResponse;
from django.template.loader import get_template
import datetime

def hello(request):
	now = datetime.datetime.now();
	html = "<html><body>It is now %s.</body></html>" % now
	return HttpResponse(html);

def main(request):
	template = get_template('main.html')
	html = template.render({'city': 'Guelph', 'active_tab': 'home'})
	return HttpResponse(html);

def profile(request):
	template = get_template('profile.html')
	html = template.render({'city': 'Guelph', 'active_tab': 'profile'})
	return HttpResponse(html);
	
def login(request):
	template = get_template('login.html')
	html = template.render({'city': 'Guelph', 'active_tab': 'login'})
	return HttpResponse(html);

def target(request):
	template = get_template('target.html')
	target = {'picture' : 'http://i.imgur.com/VBQgNPm.jpg', 'name':'Billy Generic', 'program' : 'Business', 'year': '5th', 'location' : 'Johnston'}
	html = template.render({'city': 'Guelph', 'active_tab': 'target', 'target' : target})
	return HttpResponse(html);

def base(request):
	template = get_template('base.html')
	html = template.render({'city': 'Guelph'})
	return HttpResponse(html);

