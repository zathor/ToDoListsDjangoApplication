from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from whatToDoNow.forms import LoginForm, SingupForm
from whatToDoNow.models import ToDoList, Task, Tag, EndUser
from django.contrib.auth.models import User
from django.contrib.auth.views import login as login_user
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from whatToDoNow.decorators import anonymous_required
from whatToDoNow.commands import get ,add, update, remove, edit
from whatToDoNow.commands import ajax_result_get, ajax_result_add, ajax_result_remove, ajax_result_edit, ajax_result_update

@login_required
def home(request):
	try:
		end_user = request.user.enduser
	except EndUser.DoesNotExist:
		logout(request)
		return HttpResponseRedirect(reverse("login"))
	to_do_lists = end_user.todolist_set.all()
	return render_to_response("home.html",{"user":request.user,"lists":to_do_lists},context_instance=RequestContext(request))

def confirm_user_account(request, uidb64):
	uid = urlsafe_base64_decode(uidb64)
	end_user = get_object_or_404(EndUser, user__username=uid)
	if request.user.is_authenticated():
		logout(request)
	valid_link = not end_user.confirmed
	if valid_link == True:
		end_user.confirmed = True
		end_user.save()
	return render_to_response("registration/signup_done.html",{"validlink":valid_link},context_instance=RequestContext(request))

@anonymous_required
def login(request):
	return login_user(request, authentication_form=LoginForm)

@anonymous_required
def signup(request):
	form = SingupForm()
	if request.method == 'POST':
		form = SingupForm(request=request,data=request.POST,instance=None)
		if form.is_valid():
			form.save()
			return render_to_response("registration/signup_confirm.html",context_instance=RequestContext(request))
	return render_to_response("registration/signup_form.html",{"form":form},context_instance=RequestContext(request))

@login_required
def process_operation(request):
	if request.method == 'POST':
		operation_funcs = {
			"add":add,
			"edit":edit,
			"update":update,
			"remove":remove,
			"get":get
		}

		result = operation_funcs[request.POST['operation']](request)
		if request.is_ajax():
			ajax_result_funcs = {
				"add":ajax_result_add,
				"edit": ajax_result_edit,
				"update":ajax_result_update,
				"remove":ajax_result_remove,
				"get":ajax_result_get
			}
			ret = ajax_result_funcs[request.POST['operation']](request,result)
			return HttpResponse(ret)
	return HttpResponseRedirect(reverse("home"))