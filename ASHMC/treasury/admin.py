from django.contrib import admin

from django.template.loader import render_to_string
from django.core.files import temp
from django.conf import settings
from django.http import HttpResponse

from .models import *

import subprocess
import os

class AllocationLineItemInline(admin.TabularInline):
    model = AllocationLineItem
    exclude = ('line_item',)
    readonly_fields=('amount', 'date_created', 'check_number', 'check_status')
    extra = 0

    def has_add_permission(self, request):
        return False

class AllocationAdmin(admin.ModelAdmin):
    raw_id_fields = ('for_club',)
    list_display = ('__str__', 'amount', 'amount_left', 'source', 'for_club')
    list_filter = ('school_year',)
    search_fields = ('allocation_number', 'for_club__name')
    inlines = (AllocationLineItemInline,)
    actions = ('export_as_pdf',)

    def export_as_pdf(self, request, queryset):
        allocations = queryset.all()
        pdf_files = []

        for allocation in allocations:

            # Add allocations directory to filled forms folder
            output_dir = os.path.join(settings.ASHMC_FORMS_FOLDER, 'allocations')
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

            pdf_fn = os.path.join(output_dir, '%06d.pdf' % allocation.allocation_number)
            pdf_files.append(pdf_fn)
            if not os.path.exists(pdf_fn):
                latex_fn = os.path.join(output_dir, '%06d.tex' % allocation.allocation_number)

                # Render LaTeX output
                with open(latex_fn, "wt") as latex_out:
                    print >>latex_out, render_to_string('forms/allocation_number.tex',  {'allocation': allocation})


                pdflatex = subprocess.Popen(["pdflatex", latex_fn], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=output_dir)
                while pdflatex.returncode is None:
                    output = pdflatex.communicate()
                    pdflatex.poll()

        if allocations.count() == 1:
            with open(pdf_fn, "rb") as pdf_file:
                pdf_data = pdf_file.read()
                response = HttpResponse(pdf_data, content_type='application/pdf')
                return response
        else:
            # Merge pdfs
            pdftk = subprocess.Popen(['pdftk'] + pdf_files + ['cat', 'output', '-'], stdout=subprocess.PIPE)
            output = ''
            while pdftk.returncode is None:
                output += pdftk.communicate()[0]
                pdftk.poll()

            response = HttpResponse(output, content_type='application/pdf')
            return response

    export_as_pdf.short_description = "Print PDF Forms for selected allocations"
admin.site.register(Allocation, AllocationAdmin)

class AllocationInline(admin.StackedInline):
    model = Allocation
    date_hierarchy = 'school_year__date'
    extra = 0

class OfficerInline(admin.TabularInline):
    model = Officer
    date_hierarchy = 'school_year__date'
    extra = 1
    raw_id_fields = ('student',)

class ClubAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')
    inlines = (AllocationInline, OfficerInline)
    actions = ('export_ledger_as_pdf',)

    def export_ledger_as_pdf(self, request, queryset):
        clubs = queryset.all()
        club = clubs[0]

        # Add clubs directory to filled forms folder
        output_dir = os.path.join(settings.ASHMC_FORMS_FOLDER, 'clubs')
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        pdf_fn = os.path.join(output_dir, '%s.pdf' % club.name)
        latex_fn = os.path.join(output_dir, '%s.tex' % club.name)

        # Render LaTeX output
        with open(latex_fn, "wt") as latex_out:
            print >>latex_out, render_to_string('ledgers/club.tex',  {'club': club})

        pdflatex = subprocess.Popen(["pdflatex", latex_fn], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=output_dir)
        while pdflatex.returncode is None:
            output = pdflatex.communicate()
            print output[0]
            pdflatex.poll()

        with open(pdf_fn, "rb") as pdf_file:
            pdf_data = pdf_file.read()
            response = HttpResponse(pdf_data, content_type='application/pdf')
            return response
    export_ledger_as_pdf.short_description = "Print club ledger as PDF"
admin.site.register(Club, ClubAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class AllocationLineItemInline(admin.TabularInline):
    model = AllocationLineItem
    raw_id_fields = ('allocation',)

class LineItemAdmin(admin.ModelAdmin):
    list_filter = ('account', 'check_status')
    list_display = ('date_created', 'account', 'amount', 'balance', 'description', 'check_number', 'check_status')
    search_fields = ('check_number', 'account__name')
    fieldsets = ((None, {
                'fields': ('category', 'account', 'amount', 'description')}),
                  ('Checks', {
                'fields': ('request', ('check_number', 'check_status'))}))
    raw_id_fields = ('request',)
    inlines = (AllocationLineItemInline,)
admin.site.register(LineItem, LineItemAdmin)

class FundAdmin(admin.ModelAdmin):
    pass
admin.site.register(Fund, FundAdmin)

class AccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(Account, AccountAdmin)

class BudgetItemInline(admin.TabularInline):
    model = BudgetItem

class BudgetRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('date_filed',)
    inlines = (BudgetItemInline,)

    fieldsets = (
        (None, {
            'fields': (('club', 'for_school_year'))}),
        ('Contact Information', {
            'fields': ('filer', 'mailing_address',
                       'college')}),
        ('Previous Budget Information', {
            'fields': ('attended_budgeting_for', ('did_internal_fundraising', 'internal_fundraising_amount'))}),
        ('Membership Information', {
            'fields': ('active_members', 'interest_level', ('hmc_members',
                       'scripps_members', 'cmc_members', 'pomona_members',
                       'pitzer_members', 'other_members'))}),
        ('Budget Request', {
            'fields': ('ashmc_amount', ('scripps_amount', 'pomona_amount',
                       'cmc_amount', 'pitzer_amount', 'other_amount'),
                       'other_explanation', 'budget_explanation')}),
        ('ASHMC Use Only', {
            'fields': (('approved', 'date_approved'), 'amount_allocated')}))
admin.site.register(BudgetRequest, BudgetRequestAdmin)

class LineItemInline(admin.TabularInline):
    model=LineItem
    exclude=('allocations','balance')

class CheckRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('date_filed',)
    raw_id_fields = ('filer',)
    list_display = ('club', 'year', 'date_filed', 'amount', 'date_approved', 'status')
    list_filter = ('approved',)
    search_fields = ('club__name', 'filer__name', 'payee', 'line_items__check_number')
    inlines=(LineItemInline,)

    fieldsets = (
        (None, {
            'fields': (('club', 'year'), 'filer',
                       'amount', 'payee', 'deliver_to', 'other_information')}),
        ('ASHMC Use Only', {
            'fields': (('approved', 'date_approved'), 'reason_denied',)}))
admin.site.register(CheckRequest, CheckRequestAdmin)
