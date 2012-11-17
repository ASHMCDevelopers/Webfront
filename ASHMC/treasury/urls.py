from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'ASHMC.treasury.views.overview', {}, name='fund_overview'),
    # url(r'^overview/$', 'ASHMC.treasury.views.overview', {}, name='fund_overview'),
    url(r'^funds/(?P<fund_name>.*)$', 'ASHMC.treasury.views.ledger', {}, name='ledger'),
    url(r'^clubs/admin', 'ASHMC.treasury.views.club_select', {}, name='club_select'),
    url(r'^clubs/(?P<club_name>.*)/admin$', 'ASHMC.treasury.views.club_admin', {}, name='club_admin'),
    url(r'^clubs/(?P<club_name>.*)/forms/check_request/(?P<request_id>[0-9]+)$', 'ASHMC.treasury.views.check_request', {}, name='check_request'),
    url(r'^clubs/(?P<club_name>.*)/forms/check_request$', 'ASHMC.treasury.views.new_check_request', {}, name='new_check_request'),
    url(r'^clubs/(?P<club_name>.*)/forms/budget_request$', 'ASHMC.treasury.views.new_budget_request', {}, name='new_budget_request'),
    url(r'^clubs/(?P<club_name>.*)$', 'ASHMC.treasury.views.club_detail', {}, name='club_detail'),
    url(r'^budgets/inline_item_row/(?P<number>\d+)?$', 'ASHMC.treasury.views.request_inline_item', name='ajax_item_inline_row'),
)
