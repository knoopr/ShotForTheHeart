from django.contrib.auth import authenticate, login, get_user_model
from mailin import Mailin
from string import punctuation



def authorize(request):
	email = request.POST.get('Email')
	password = request.POST.get('Password')
	if len(email) < 6 or len(password) < 10:
		return {'ERROR' : 'Too short'}
	else:
		user = authenticate(username = email, password = password)
		if user is not None:
			login(request,user)
			return {'VALID' : 'Logged in succesfully'}
		else:
			return {'ERROR' : 'Username or password incorrect!'}
		
	return {'ERROR' : 'An unknown error occurred'}
	
	
def check_password(password, confirm):
	if password != confirm:
		return {'ERROR' : 'The two passwords do not match.'}
	
	elif len(password) < 10:
		return {'ERROR' : 'The password is too short.'}

	security_combo = [0,0,0]
	for c in password:
		if c.isupper():
			security_combo[0] = 1
		elif c.isalpha():
			security_combo[1] = 1
		elif c.isdigit():
			security_combo[2] = 1
		elif c in punctuation:
			security_combo[2] = 1
	if 0 in security_combo:
		return {'ERROR' : 'Password is not complex enough. Password requires 1 lower, 1 upper and 1 symbol or number.'}
		
	return {'VALID' : 'Good'}


def register(request):
	email = request.POST.get('Email')
	password = request.POST.get('Password')
	confirm = request.POST.get('confirmPassword')
	security_check = check_password(password, confirm)
	if 'ERROR' in security_check:
		return security_check
	else:
		user = get_user_model().objects.create_user(email=email, password=password)
		if 'VALID' in user:
			#return user;
			user_object = user['VALID']
			Send_registration_email(user_object.user_email,user_object.activation_url);
			return user
		else:
			return user
			
			
def Send_registration_email(emailAddress, activation_url):
	file = open('/var/www/html/ShotForTheHeart/ShotForTheHeart/Credentials').read()
	credentials = eval(file)
	mailSystem = Mailin("https://api.sendinblue.com/v2.0", credentials['email'])
	message = {
		'to' : {'knoop.rick@gmail.com':'Rick Knoop'},
		'from' : ['sftheart@uoguelph.ca' , 'Shot for the heart Guelph'],
		'subject' : 'Activate your account',
		'html' : 'Hello<br>You recently decided to register for an account at the Shot for the Heart website. Please click the link below to activate your account.<br><br>http://shotfortheheart.ca/register/'+activation_url+'<br><br>Thanks,<br>Shot for the Heart system administator.',
	}
	result = mailSystem.send_email(message)
	if 'failure' in result['code']:
		try:
			file = open('/var/www/html/ShotForTheHeart/emailError.log', 'w+')
			file.write(str(timezone.now)+' email address: '+str(user_email)+' Error information: '+str(result)+'\n\n')
			file.close()
		except:
			pass
		return {'ERROR': 'Your account was created correctly, but the email failed. Please contact sftheart@uoguelph.ca'}
	else:
		return {'VALID': 'Everything worked succesfully'}