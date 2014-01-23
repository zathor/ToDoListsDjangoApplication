from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.template import loader
from django.utils.encoding import force_bytes

status_choices = [
	('To Do','To Do'),
	('In Progress','In Progress'),
	('Done','Done')]

# EndUser Model
class EndUser(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	confirmed = models.BooleanField(default=False)

	def email_user(self, subject, message):
		"""
		Sends an email to this User.
		"""
		email = EmailMessage(subject, message, to = [self.user.email])
		email.send()

	def send_account_confirmation_email(self, request,
			subject_template_name="registration/user_confirm_subject.txt",
			email_template_name="registration/user_confirm_email.html",
			 domain_override=None, use_https=False, token_generator=default_token_generator):
		"""
		Generates a link for account activation and sends to user.
		"""
		if not domain_override:
			current_site = get_current_site(request)
			site_name = current_site.name
			domain = current_site.domain
		else:
			site_name = domain = domain_override
		c = {
			'email': self.user.email,
			'domain': domain,
			'site_name': site_name,
			'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
			'user': self.user,
			'protocol': 'https' if use_https else 'http',
		}
		subject = loader.render_to_string(subject_template_name, c)
		# Email subject *must not* contain newlines
		subject = ''.join(subject.splitlines())
		email = loader.render_to_string(email_template_name, c)
		self.email_user(subject=subject,message=email)

	def __unicode__(self):
		return self.user.username

# To-Do List Model
class ToDoList(models.Model):
	name = models.CharField(verbose_name="list name", max_length=255, blank=False)
	status = models.CharField(
		verbose_name="status",
		max_length=15,
		blank=False,
		choices=status_choices)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
	created_by = models.ForeignKey(User, null=False, blank=False)

# Task Model
class Task(models.Model):
	task = models.TextField(verbose_name="task", max_length=255, blank=False)
	status = models.CharField(
		verbose_name="status",
		max_length=15,
		blank=False,
		choices=status_choices)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
	to_do_list = models.ForeignKey(ToDoList, null=False, blank=False)

# Tag Model

class Tag(models.Model):
	tag = models.SlugField(
		verbose_name="tag",
		max_length=30,
		unique=True,
		blank=False,
		db_index=True)
	tasks = models.ManyToManyField(Task, null=False, blank=False)