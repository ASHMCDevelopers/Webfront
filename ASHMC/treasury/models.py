from django.db import models, transaction
from django.core.exceptions import ObjectDoesNotExist

import datetime


class TreasuryYearManager(models.Manager):
    def get_current(self):
        '''Gets the current TreasuryYear'''
        now = datetime.datetime.now()

        # The ASHMC Treasury Year starts in May
        if now.month < 5:
            year = now.year - 1
        else:
            year = now.year

        # Treasury years span New Years
        description = '%04d-%04d' % (year, year + 1)
        try:
            return self.get(description=description)
        except ObjectDoesNotExist:
            return TreasuryYear.objects.create(
                description=description,
                date=datetime.date(year, 5, 1),
            )


class TreasuryYear(models.Model):
    '''Represents an ASHMC Treasury Year (Slightly different from normal school years)'''

    description = models.CharField(  # The string (i.e., '2012-2013') representation of this school year
        max_length=9,
        unique=True,
        db_index=True,
    )
    date = models.DateField()  # The start date of the treasury year

    objects = TreasuryYearManager()

    def __unicode__(self):
        return u"{}".format(self.description)


# Classes involving bank ledgers

class Account(models.Model):
    name = models.CharField(
        help_text='The name of the ASHMC account',
        max_length=200,
    )
    description = models.TextField()

    def __unicode__(self):
        return u"{}".format(self.name)


class FundManager(models.Manager):
    def get_default(self):
        '''Get a default fund source. Defaults to a fund named Unresolved'''
        try:
            return self.get(name='Unresolved')
        except Fund.DoesNotExist:
            return Fund.objects.create(
                name='Unresolved',
                description='Fake account for unresolved allocations'
            )


class Fund(models.Model):
    '''An ASHMC fund, like the long-term fund, or club budgets, etc.'''

    name = models.CharField(
        help_text='The name of the fund',
        max_length=200,
        unique=True,
    )
    account = models.ForeignKey(
        'Account',
        related_name='funds',
        null=True,
    )
    description = models.TextField()

    objects = FundManager()

    @property
    def currently_allocated(self):
        '''Get sum total of current allocations'''
        return self.allocations.filter(school_year=TreasuryYear.objects.get_current()).aggregate(models.Sum('amount'))['amount__sum'] or 0

    @property
    def currently_free(self):
        '''Get amount of money that has not been allocated'''
        expenses = self.line_items.filter(request__year=TreasuryYear.objects.get_current()).aggregate(models.Sum('amount'))['amount__sum'] or 0
        return self.balance + expenses - self.currently_allocated

    @property
    def balance(self):
        '''Get balance available for this fund.'''
        if self.line_items.count() == 0:
            return 0
        return self.line_items.all()[0].balance

    @property
    def bank_amount(self):
        '''The amount actually in the bank, taking into account checks that are still pending.'''

        # We get the balance and add back in the total amount of pending checks
        total_pending = self.line_items.filter(check_status=LineItem.PENDING).aggregate(models.Sum('amount'))['amount__sum'] or 0
        return self.balance + total_pending

    def __unicode__(self):
        return u"{}".format(self.name)


class Allocation(models.Model):
    '''Represents an allocation given from ASHMC. Every allocation has a fund from which the money comes.'''

    def new_allocation_number():
        '''Coin a new allocation number, by incrementing the highest allocation number'''
        num = Allocation.objects.all().aggregate(models.Max('allocation_number'))['allocation_number__max']
        if num is None:
            num = 0
        return num + 1

    # Administrative information
    allocation_number = models.IntegerField(
        default=new_allocation_number,
        unique=True
    )
    school_year = models.ForeignKey(TreasuryYear, default=TreasuryYear.objects.get_current)
    for_club = models.ForeignKey('Club', blank=True, null=True, related_name='allocations')

    # Monetary information
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    amount_requested = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    source = models.ForeignKey(Fund, default=Fund.objects.get_default, related_name='allocations')

    # ASHMC approvals/etc.
    date_approved = models.DateTimeField(
        help_text='The date the ASHMC council approved this allocation',
        null=True,
        blank=True,
    )

    explanation = models.TextField(
        help_text="Additional stipulations for use of funds or general comments",
        default="",
        blank=True,
    )

    @property
    def amount_left(self):
        '''The amount left in this allocation.'''
        total_spent = self.allocation_line_items.all().aggregate(models.Sum('amount'))['amount__sum'] or 0
        return self.amount - total_spent

    def __unicode__(self):
        return u'Allocation %06d' % self.allocation_number

    class Meta:
        ordering = ('allocation_number', )


class Club(models.Model):
    '''An ASHMC Club'''

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
    )
    description = models.TextField()

    date_founded = models.DateField(null=True, blank=True)
    date_ended = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('name', )

    @property
    def line_items(self):
        # You have to go through the request object to find line items belonging to this club
        return LineItem.objects.filter(request__club=self)

    @property
    def balance(self):
        '''The amount of funds still available for this club'''
        spent = self.current_allocations.aggregate(models.Sum('allocation_line_items__amount'))['allocation_line_items__amount__sum'] or 0
        return self.current_allocation - spent

    @property
    def current_allocation(self):
        '''The sum total of all allocations made to this club for the current school year'''
        return self.current_allocations.aggregate(models.Sum('amount'))['amount__sum'] or 0

    @property
    def current_allocations(self):
        '''The QuerySet of all allocations available to the club for this school year'''
        return self.allocations.filter(school_year=TreasuryYear.objects.get_current())

    @property
    def current_budget_requests(self):
        '''The QuerySet of all budget requests for this club for this school year'''
        return self.budget_requests.filter(for_school_year=TreasuryYear.objects.get_current())

    @property
    def current_officers(self):
        '''The QuerySet of this year's club officers'''
        return self.officers.filter(school_year=TreasuryYear.objects.get_current())

    @property
    def current_officers_for_allocation(self):
        '''Gets list of club officers as it should appear on the allocation notification form. Includes the empty slots as well'''
        officers = list(self.officers.filter(school_year=TreasuryYear.objects.get_current())[:5])
        officers += [{'position': '', 'student': ''}] * (5 - len(officers))
        return officers

    def str_id(self):
        '''Correctly formats the club number'''
        return '%06d' % self.id

    def __unicode__(self):
        return u"%s" % (self.name, )


class Officer(models.Model):
    '''Represents a club officer. These are the people who can sign for checks'''

    club = models.ForeignKey('Club', related_name='officers')
    school_year = models.ForeignKey('TreasuryYear', default=TreasuryYear.objects.get_current)

    student = models.ForeignKey('main.Student', related_name='club_positions')
    position = models.CharField(max_length=512, blank=False, null=False)

    main_contact = models.BooleanField(help_text='Whether this officer is the club\'s main contact for the school year')

    is_club_superuser = models.BooleanField(help_text='Whether this officer can access and change this club\'s treasury information', default=True)

    def __unicode__(self):
        return u'%s %s of %s' % (self.school_year, self.position, self.club)

    class Meta:
        unique_together = ('club', 'school_year', 'student')  # Ensure each member is listed only once


class CategoryManager(models.Manager):
    def get_default(self):
        try:
            return self.get(name='Miscellaneous')
        except Category.DoesNotExist:
            category = Category(name='Miscellaneous', description='Miscellaneous/Uncategorized items')
            category.save()
            return category


class Category(models.Model):
    '''Categories for line items'''

    name = models.CharField(max_length=200)
    description = models.TextField()

    objects = CategoryManager()

    def __unicode__(self):
        return u"{}".format(self.name)


class LineItem(models.Model):
    '''A line item in a fund ledger'''

    PENDING = 'Pending'
    RECONCILED = 'Reconciled'

    account = models.ForeignKey('Fund', related_name='line_items')
    date_created = models.DateTimeField(auto_now_add=True)

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='The balance left after this line item was committed to the ledger')

    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='The amount this line item withdrew from the ledger (negative values indicate a deposit)')

    description = models.CharField(max_length=300, help_text='Description of what this money was spent on')

    check_number = models.IntegerField(null=True, blank=True, help_text='The number of the check used to pay for this line item')

    check_status = models.CharField(max_length=100, choices=((PENDING, 'Pending bank approval'),
                                                             (RECONCILED, 'Check cashed')), default=PENDING, help_text='Indicates whether or not this check has been cashed')

    allocations = models.ManyToManyField('Allocation', related_name='line_items', through='AllocationLineItem')  # The allocations from which this line item came. These are created automatically, when the line item is added
    request = models.ForeignKey('CheckRequest', null=True, related_name='line_items', blank=True)  # The check request (if any) that spawned this line item
    category = models.ForeignKey('Category', null=True, default=Category.objects.get_default, help_text='Line item\'s category. Helps with taxes, etc.')

    @property
    def prev_balance(self):
        try:
            balance = self.account.line_items.filter(date_created__lt=self.date_created)[0].balance
        except:
            balance = 0
        return balance

    def clean(self):
        # Update the appropriate balances, depending on this line item's amount
        if self.pk is None:
            # If we're being created, a simple subtraction suffices
            self.balance = self.account.balance - self.amount
            total = -1
        else:
            # Update all line items after this, if the balances don't add up
            balance = self.prev_balance
            if self.balance != (balance - self.amount):
                self.balance = balance - self.amount
                prev_balance = self.balance
                for line_item in self.account.line_items.filter(date_created__gt=self.date_created).order_by('date_created'):
                    prev_balance = line_item._update_balance(prev_balance)
                    line_item.save()

            # Check that there is enough money left
            total = self.allocation_line_items.all().aggregate(models.Sum('amount'))['amount__sum'] or 0

        if total != self.amount and self.request is not None:
            allocations = self.request.club.allocations.filter(source=self.account, school_year=TreasuryYear.objects.get_current())  # Only get allocations for this year and from the same account
            total_amount_left = 0
            for allocation in allocations:
                total_amount_left += allocation.amount_left
            if total_amount_left < self.amount:
                # There's not enough allocation
                from django.core.exceptions import ValidationError
                raise ValidationError('Insufficient funds')

    def _update_balance(self, prev_balance):
        self.balance = prev_balance - self.amount
        return self.balance

    @staticmethod
    def post_save(sender, **kwargs):
        # Adds the appropriate line items to the allocations used by this line item.
        # We get the club this line item was for, and then withdraw amounts in the order of the
        # allocations. If there are insufficient funds, we throw an exception
        self = kwargs['instance']

        total = self.allocation_line_items.all().aggregate(models.Sum('amount'))['amount__sum'] or 0

        if total != self.amount and self.request is not None:
            AllocationLineItem.objects.filter(line_item=self).delete()
            with transaction.commit_on_success():  # We want this to be atomic
                # Find allocations based on account source
                allocations = self.request.club.allocations.filter(source=self.account, school_year=TreasuryYear.objects.get_current())  # Only get allocations for this year and from the same account

                amount_left = self.amount  # The amount remaining after withdrawing money from allocations
                for allocation in allocations:
                    if allocation.amount_left > amount_left:
                        AllocationLineItem(line_item=self, allocation=allocation, amount=amount_left).save()
                        amount_left = 0
                        break
                    else:
                        amount_left -= allocation.amount_left
                        AllocationLineItem(line_item=self, allocation=allocation, amount=allocation.amount_left).save()
                if amount_left > 0:
                    # There's not enough allocation
                    from django.core.exceptions import ValidationError
                    raise ValidationError('Insufficient funds')

    class Meta:
        ordering = ('-date_created', )
models.signals.post_save.connect(LineItem.post_save, sender=LineItem)


class AllocationLineItem(models.Model):
    '''Line items for allocations. These objects are created automatically,
    whenever a line item is assocatied with a request'''

    line_item = models.ForeignKey('LineItem', related_name='allocation_line_items')
    allocation = models.ForeignKey('Allocation', related_name='allocation_line_items')

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def date_created(self):
        return self.line_item.date_created

    @property
    def check_number(self):
        return self.line_item.check_number

    @property
    def check_status(self):
        return self.line_item.check_status


class BudgetRequest(models.Model):
    club = models.ForeignKey('Club', related_name='budget_requests')
    date_filed = models.DateTimeField(auto_now=True)

    for_school_year = models.ForeignKey('TreasuryYear', default=TreasuryYear.objects.get_current)

    filer = models.ForeignKey('main.Student')

    attended_budgeting_for = models.CharField(
        'Which budget hearings did you attend last year?',
        max_length=32,
        choices=(('None', 'None'),
            ('HMC', 'Harvey Mudd College'),
            ('5C', '5C')),
        default='None')

    # Membership info
    active_members = models.IntegerField(help_text="How many members consistently show up at meetings?")
    interest_level = models.IntegerField(help_text="How many members are interested (say from a mailing list)")

    hmc_members = models.IntegerField('HMC')
    scripps_members = models.IntegerField('Scripps')
    cmc_members = models.IntegerField('CMC')
    pomona_members = models.IntegerField('Pomona')
    pitzer_members = models.IntegerField('Pitzer')
    other_members = models.IntegerField('Other')

    # Budget info
    did_internal_fundraising = models.BooleanField('Have you done internal fundraising?')
    internal_fundraising_amount = models.DecimalField(
        'Amount',
        decimal_places=2,
        max_digits=11,
        blank=True,
        null=True
    )

    # Budget request
    ashmc_amount = models.DecimalField('ASHMC request', decimal_places=2, max_digits=11)
    scripps_amount = models.DecimalField(decimal_places=2, max_digits=11)
    pomona_amount = models.DecimalField(decimal_places=2, max_digits=11)
    cmc_amount = models.DecimalField('CMC amount', decimal_places=2, max_digits=11)
    pitzer_amount = models.DecimalField(decimal_places=2, max_digits=11)
    other_amount = models.DecimalField(decimal_places=2, max_digits=11)
    other_explanation = models.TextField(help_text='Please explain your other source of funding')

    budget_explanation = models.TextField(help_text='Please explain why your club deserves funding, or anything else that needs to be made clear', blank=True, null=True)

    # ASHMC Use Only
    approved = models.BooleanField(default=False)
    date_approved = models.DateTimeField(null=True, blank=True)
    amount_allocated = models.DecimalField(max_digits=11, decimal_places=2, null=True)

    def __unicode__(self):
        return u"Budget Request for %s requesting %s on %s" % (self.club, self.ashmc_amount, self.date_filed)

    @property
    def denied(self):
        return self.date_approved is not None and not self.approved

    @property
    def status(self):
        '''String representation of the check status'''
        if self.approved:
            return 'Approved'
        elif self.denied:
            return 'Denied'
        else:
            return 'Pending'


class BudgetItem(models.Model):
    budget = models.ForeignKey(BudgetRequest, related_name='budget_items')
    item = models.CharField(max_length=512)
    description = models.CharField(max_length=1024)
    amount = models.DecimalField(max_digits=11, decimal_places=2)


class CheckRequest(models.Model):
    '''A request for an ASHMC check'''

    REIMBURSEMENT = 'Reimbursement'
    UPFRONT = 'Upfront'
    SEMESTER = 'Semester'
    ENTIRE_YEAR = 'Entire year'

    club = models.ForeignKey(Club, null=True, related_name='check_requests')
    year = models.ForeignKey(TreasuryYear, null=True, default=TreasuryYear.objects.get_current)

    date_filed = models.DateTimeField(auto_now=True)

    filer = models.ForeignKey('main.Student', help_text='The student making the request')

    amount = models.DecimalField(max_digits=11, decimal_places=2)

    payee = models.CharField(max_length=512, blank=False)
    deliver_to = models.CharField(max_length=1024, help_text='If different from payee. Include mailbox, if needed', blank=True, null=True)

    request_type = models.CharField(max_length=20, choices=((REIMBURSEMENT, 'Reimbursement for past expenses'),
                                                            (UPFRONT, 'Upfront payment for planned purchase'),
                                                            (SEMESTER, 'Entire allocation for semester'),
                                                            (ENTIRE_YEAR, 'Entire allocation for year (requires council approval)')), default=REIMBURSEMENT)

    other_information = models.TextField(help_text='Is there anything else we should know?', blank=True, null=True)

    # Approved/denied information
    # If the date_approved is not None, and approved is False, the request is considered denied
    approved = models.BooleanField(default=False)
    date_approved = models.DateTimeField(null=True, blank=True)
    reason_denied = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-date_filed', )

    def __unicode__(self):
        return u'Check Request for %s on %s (%s)' % (self.club.name, self.date_filed, self.amount)

    @property
    def denied(self):
        return self.date_approved is not None and not self.approved

    @property
    def status(self):
        '''String representation of the check status'''
        if self.approved:
            return 'Approved'
        elif self.denied:
            return 'Denied'
        else:
            return 'Pending'
