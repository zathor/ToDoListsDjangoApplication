from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from whatToDoNow.models import EndUser

class LoginForm(AuthenticationForm):

	def __init__(self,request = None,*args,**kwargs):
		# Save request for further processing
		self.request = request
		super(LoginForm,self).__init__(*args,**kwargs)
		self.error_messages['not_enduser'] = "Sorry. %(username)s is not signed up."

	def clean(self):
		try:
			self.cleaned_data['username'] = username = self.cleaned_data.get('username').lower()
		except:
			username = ""
		super(LoginForm,self).clean()
		if username != "":
			try:
				end_user = EndUser.objects.get(user__username=username)
			except EndUser.DoesNotExist:
				raise forms.ValidationError(
					self.error_messages['not_enduser'],
					code='not_enduser',
					params={"username":username}
				)
		return self.cleaned_data


class SingupForm(UserCreationForm):
	def __init__(self,request = None,*args,**kwargs):
		# Save request for further processing
		self.request = request
		super(SingupForm,self).__init__(*args,**kwargs)
		self.error_messages['duplicate_email'] = "This email address is already in use. Please supply a different email address."

	class Meta:
		model = User
		fields = ("username", "first_name","last_name", "email")

	email = forms.RegexField(label="Email",
		regex=r'^([-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4})$',
		error_messages={'invalid': "This is not a valid email address."}
	)

	def clean_email(self):
		"""Validate that the supplied email address is unique for the site."""
		if User.objects.filter(email__iexact=self.cleaned_data['email']):
			raise forms.ValidationError(
				self.error_messages['duplicate_email'],
				code='duplicate_email',
			)
		return self.cleaned_data['email']

	def clean_username(self):
		try:
			self.cleaned_data['username'] = self.cleaned_data['username'].lower()
		except:
			pass
		return super(SingupForm,self).clean_username()

	def save(self, commit=True):
		user = super(SingupForm, self).save(commit=False)
		user.username = user.username.lower()
		user.is_staff = False
		user.is_superuser = False
		end_user = EndUser(user=user)
		end_user.send_account_confirmation_email(request=self.request)
		user.save()		
		end_user.save()
		return user