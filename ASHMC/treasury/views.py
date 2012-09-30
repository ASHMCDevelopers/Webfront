from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .models import *
from . import forms

def club_permissions_required(f):
    '''A decorator for functions requiring that the current user have permissions for the given
    club. The club_name parameter must be specified as a request parameter'''
    def new_func(request, *args, **kwargs):
        # Get the club from the request
        club = get_object_or_404(Club, name=kwargs['club_name'])
        user = request.user
        # If the user is a superuser, s/he has access to every club.
        if not user.is_superuser:
            try:
                officer_entry = club.current_officers.get(student=user.student)
            except Officer.DoesNotExist:
                return redirect('login')
            # If the officer doesn't have club permissions, redirect
            if not officer_entry.is_club_superuser:
                return redirect('login')
        return f(request, *args, **kwargs)
    new_func.__name__ = f.__name__
    return new_func

@login_required
def club_detail(request, club_name):
    '''Public-viewable club detail'''
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
    '''Let's the user create a new check request'''
    club = get_object_or_404(Club, name=club_name)
    if request.method == 'POST':
        form = forms.CheckRequestForm(request.POST)
        if form.is_valid():
            new_check_request = form.save(commit=False)

            # Set default parameters
            new_check_request.club = club
            new_check_request.filer = request.user.student

            new_check_request.save()
            return redirect('club_admin', club_name=club_name)
    else:
        form = forms.CheckRequestForm()

    return render_to_response('requests/new_check_request.html',
                              context_instance=RequestContext(request, {'form': form, 'club': club}))

@login_required
@club_permissions_required
def budget_request(request, club_name):
    '''Let's the user create a new budget request'''
    club = get_object_or_404(Club, name=club_name)
    if request.method == 'POST':
        form = forms.BudgetRequestForm(request.POST)
        if 'add-more' in request.POST:
            post_data = request.POST.copy()
            post_data['budget_items-TOTAL_FORMS'] = int(post_data['budget_items-TOTAL_FORMS']) + 5,
            items = forms.BudgetItemFormSet(post_data)
        else:
            items = forms.BudgetItemFormSet(request.POST)
            if form.is_valid():
                print 'form valid'
                if items.is_valid():
                    print 'items valid'
                    request_instance = form.save(commit=False)
                    items = forms.BudgetItemFormSet(request.POST, instance=request_instance)

                    request_instance.club = club
                    request_instance.filer = request.user.student
                    request_instance.save()

                    items.save()
                    return redirect('club_admin', club_name=club_name)
    else:
        form = forms.BudgetRequestForm()
        items = forms.BudgetItemFormSet()

    return render_to_response('requests/new_budget_request.html',
                              context_instance=RequestContext(request, {'form': form, 'items': items,'club': club}))

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
    accounts = Fund.objects.all()
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
def ledger(request, fund_name):
    fund = get_object_or_404(Fund, name=fund_name)
    return render_to_response('ledger/ledger.html',
                              context_instance=RequestContext(request, {'fund': fund}))
