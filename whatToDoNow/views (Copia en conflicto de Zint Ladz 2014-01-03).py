from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from whatToDoNow.forms import LoginForm, SingupForm
from whatToDoNow.models import ToDoList, Task, Tag
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from whatToDoNow.models import EndUser

def home(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse("login"))
	return render_to_response("home.html",{"user":request.user},context_instance=RequestContext(request))

def confirm_user_account(request):
	return HttpResponseRedirect(reverse("login"))

def login(request):
	form = LoginForm()
	if request.method == 'POST':
		try:
			print request.POST
			username = request.POST['username'].lower()
			print username
			end_user = EndUser.objects.get(user__username==username)
			print end_user
			if end_user.confirmed:
				password = request.POST['password']
				user = authenticate(username=username,password=password)
				if user is not None:
					if user.is_active:
						login(request,user)
						return render_to_response("home.html",{"user": user},context_instance=RequestContext(request))
					else:
						form.add_form_error("Opss! Sorry. Looks like your account has been disabled.")
						print form.get_form_errors()
				else:
					form.add_form_error("Opss! Looks like password is incorrect.")
					form.add_form_error("Note that field are case-sensitive.")
			else:
				email_verification_form.add_form_error("Sorry, but your account have not been confirmed.")
				return render_to_response("registration/send_email_verification.html",{"email_verification_form": email_verification_form},context_instance=RequestContext(request))
		except EndUser.DoesNotExists:
			login_form.add_form_error("Opss! Sorry, but "+ username +" is not a registered user.")
		except:
			login_form.add_form_error("Opss! Looks like something went wrong. Please try again.")
	return render_to_response("registration/login.html",{"login_form": login_form},context_instance=RequestContext(request))

def signup(request):
	form = SingupForm()
	if not request.user.is_authenticated():
		if request.method == 'POST':
			form = SingupForm(request=request,data=request.POST,instance=None)
			if form.is_valid():
				form.save()
				return render_to_response("registration/signup_done.html",{"form":form},context_instance=RequestContext(request))
	return render_to_response("registration/signup_form.html",{"form":form},context_instance=RequestContext(request))

def logout(request):
	return render_to_response("registration/logged_out.html",context_instance=RequestContext(request))

def password_reset(request):
	return render_to_response("registration/password_reset_form.html",context_instance=RequestContext(request))

def password_change(request):
	return render_to_response("registration/password_change_form.html",context_instance=RequestContext(request))