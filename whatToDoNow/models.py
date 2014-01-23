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
	('Done','Done')
]

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
			'uid': urlsafe_base64_encode(force_bytes(self.user.username)),
			'user': self.user,
			'protocol': 'https' if use_https else 'http',
		}
		subject = loader.render_to_string(subject_template_name, c)
		# Email subject *must not* contain newlines
		subject = ''.join(subject.splitlines())
		email = loader.render_to_string(email_template_name, c)
		self.email_user(subject=subject,message=email)

	def add_to_do_list(self, list_name):
		to_do_list = ToDoList(name=list_name,created_by=self)
		to_do_list.save()
		return to_do_list

	def __unicode__(self):
		return self.user.username

# To-Do List Model
class ToDoList(models.Model):
	name = models.CharField(verbose_name="list name", max_length=255, blank=False)
	status = models.PositiveIntegerField(verbose_name="progress status",null=False,default=0)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
	created_by = models.ForeignKey(EndUser, null=False, blank=False)

	def add_task(self,task_name):
		task = Task(task=task_name,status=status_choices[0][1],to_do_list=self)
		task.save()
		return task

	def edit(self,list_name):
		self.name = list_name
		self.save()
		return self

	def progress(self):
		try:
			self.status = self.task_set.filter(status="Done").count() / float(self.task_set.count())
		except ZeroDivisionError:
			self.status = 0
		self.save()
		return self.status * 100

	def __unicode__(self):
		return self.name

# Task Model
class Task(models.Model):
	task = models.CharField(verbose_name="task", max_length=255, blank=False)
	status = models.CharField(
		verbose_name="status",
		max_length=15,
		blank=False,
		choices=status_choices)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
	to_do_list = models.ForeignKey(ToDoList, null=False, blank=False)

	def get_tags_str(self):
		return ", ".join([str(tag) for tag in self.tag_set.all()])

	def add_tag(self,tag_name):
		try:
			tag = Tag.objects.get(tag=tag_name)
		except Tag.DoesNotExist:
			tag = Tag(tag=tag_name)
			tag.save()
		tag.add_task(self)
		return tag

	def edit(self,task_name):
		self.task = task_name
		self.save()
		return self

	def update_status(self,task_status):
		if self.status == task_status:
			return False
		self.status = task_status
		self.save()
		return self

	def remove_tag(self,tag):
		return tag.remove_task(self)

	def __unicode__(self):
		return self.task

# Tag Model

class Tag(models.Model):
	tag = models.SlugField(
		verbose_name="tag",
		max_length=30,
		unique=True,
		blank=False,
		db_index=True)
	tasks = models.ManyToManyField(Task, null=False, blank=False)

	def add_task(self,task):
		if not task in self.tasks.all():
			self.tasks.add(task)
			self.save()
			return True
		return False

	def remove_task(self,task):
		if task in self.tasks.all():
			self.tasks.remove(task)
			return True
		return False

	def edit(self,tag_name):
		self.tag = tag_name
		self.save()
		return self

	def __unicode__(self):
		return self.tag

# Adding extra funcionality to User model

def username_pretty(self):
	return self.username[0:1].upper() + self.username[1:].lower()

User.add_to_class('username_pretty',username_pretty)