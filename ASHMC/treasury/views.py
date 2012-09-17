from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .models import *
from . import forms

def club_permissions_required(f):
    def new_func(request, *args, **kwargs):
        club = get_object_or_404(Club, name=kwargs['club_name'])
        user = request.user
        if not user.is_superuser:
            try:
                officer_entry = club.current_officers.get(student=user.student)
            except Officer.DoesNotExist:
                return redirect('login')
            if not officer_entry.is_club_superuser:
                return redirect('login')
        return f(request, *args, **kwargs)
    new_func.__name__ = f.__name__
    return new_func

@login_required
def club_detail(request, club_name):
    club = get_object_or_404(Club, name=club_name)
    return render_to_response('clubs/detail.html',
                              context_instance=RequestContext(request, {'club': club}))

@login_required
@club_permissions_required
def club_admin(request, club_name):
    club = get_object_or_404(Club, name=club_name)
    user = request.user
    return render_to_response('clubs/admin.html',
                              context_instance=RequestContext(request, {'club': club}))

@login_required
@club_permissions_required
def check_request(request, club_name):
    club = get_object_or_404(Club, name=club_name)
    if request.method == 'POST':
        form = forms.CheckRequestForm(request.POST)
        if form.is_valid():
            new_check_request = form.save(commit=False)
            new_check_request.club = club
            new_check_request.filer = request.user.student
            new_check_request.save()
            return redirect('club_admin', club_name=club_name)
    else:
        form = forms.CheckRequestForm()

    return render_to_response('requests/new_check_request.html',
                              context_instance=RequestContext(request, {'form': form, 'club': club}))

@login_required
def club_select(request):
    if request.user.is_superuser:
        clubs = Club.objects.all()
    else:
        officers = request.user.student.club_positions.filter(is_club_superuser=True)
        clubs = [officer.club for officer in officers]
    return render_to_response('clubs/select.html',
                              context_instance=RequestContext(request, {'clubs': clubs}))

@login_required
def overview(request):
    accounts = Account.objects.all()
    clubs = Club.objects.all()

    total_funds = sum([account.balance for account in accounts])
    total_allocated = sum([account.currently_allocated for account in accounts])
    total_free = sum([account.currently_free for account in accounts])

    return render_to_response('treasury/overview.html',
                              context_instance=RequestContext(request,{'accounts': accounts, 'clubs': clubs,
                                                                       'total_funds': total_funds,
                                                                       'total_allocated': total_allocated,
                                                                       'total_free': total_free}))

@login_required
def ledger(request, account_name):
    account = get_object_or_404(Account, name=account_name)
    return render_to_response('ledger/ledger.html',
                              context_instance=RequestContext(request, {'account': account}))
