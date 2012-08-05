from django.conf.urls import patterns, include, url
from django.conf import settings
from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ASHMC.views.home', name='home'),
    # url(r'^ASHMC/', include('ASHMC.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^courses/', include('ASHMC.courses.urls')),

    url(r'^blog/', include('blogger.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^legal/', include('ASHMC.legal.urls')),
    url(r'^vote/', include('ASHMC.vote.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
    # DON'T user the soft_link if you can avoid it.
    url(r'^soft_link/(?P<url_name>.*)/', lambda x, url_name: redirect(url_name)),
    url(r'^', include('ASHMC.main.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
