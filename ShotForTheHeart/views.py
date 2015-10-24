from django.http import HttpResponse;
from django.template.loader import get_template
import datetime

def hello(request):
	now = datetime.datetime.now();
	html = "<html><body>It is now %s.</body></html>" % now
	return HttpResponse(html);

def base(request):
	template = get_template('base.html')
	html = template.render({'city': 'Guelph'})
	return HttpResponse(html);
