from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'whatToDoNow.views.home', name='home'),
	url(r'^signup/?$', 'whatToDoNow.views.signup', name='signup'),
	url(r'^confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/?$',
		'whatToDoNow.views.confirm_user_account',
		name='confirm_user_account'),
	url(r'^process_operation/?$', 'whatToDoNow.views.process_operation', name='process_operation'),
	url(r'^login/?$','whatToDoNow.views.login',name='login'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'', include('django.contrib.auth.urls')),
)

#urlpatterns += patterns('',
	# Examples:
#     url(r'^$', 'whatToDoNow.views.home', name='home'),
#     url(r'^signup/?$', 'whatToDoNow.views.signup', name='signup'),
#     #url(r'^login/?$', 'whatToDoNow.views.login', name='login'),
#     url(r'^login/?$', 'django.contrib.auth.views.login', name='login'),
#     url(r'^logout/?$', 'django.contrib.auth.views.logout', name='site_logout'),
#     url(r'^password_reset/?$', 'django.contrib.auth.views.password_reset', name='password_reset'),
#     url(r'^password_reset_done/?$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
#     url(r'^password_change/?$', 'django.contrib.auth.views.password_change', name='password_change'),
#     # url(r'^blog/', include('blog.urls')),
#     url(r'^admin/', include(admin.site.urls)),
# )