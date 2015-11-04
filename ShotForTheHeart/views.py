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
	html = template.render({'city': 'Guelph', 'active_tab': 'profile', 'picture': 'http://i.imgur.com/VBQgNPm.jpg', 'target' : target})
	return HttpResponse(html);	

def base(request):
	template = get_template('base.html')
	html = template.render({'city': 'Guelph'})
	return HttpResponse(html);

