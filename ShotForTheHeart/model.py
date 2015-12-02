def authorize(request):
	email = request.POST.get('Email')
	password = request.POST.get('Password')
	if email == None:
		return {'ERROR': 'Empty Email'}
	elif password == None:
		return {'ERROR': 'Empty Password'}
	elif len(email) < 6 or len(password) < 8:
		return {'ERROR' : 'Too short'}