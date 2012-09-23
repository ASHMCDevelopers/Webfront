from django.db import models, transaction
from django.core.exceptions import ObjectDoesNotExist

import datetime

class TreasuryYear(models.Model):
    '''Represents an ASHMC Treasury Year (Slightly different from normal school years)'''

    description=models.CharField(max_length=9, unique=True, db_index=True)
    date=models.DateField()

    @classmethod
    def get_current(cls):
        now = datetime.datetime.now()

        if now.month < 7:
            year = now.year - 1
        else:
            year = now.year

        description = '%04d-%04d' % (year, year+1)
        try:
            return TreasuryYear.objects.get(description=description)
        except ObjectDoesNotExist:
            ret = TreasuryYear(description=description, date=datetime.date(year,9, 1))
            ret.save()
            return ret

    def __str__(self):
        return self.description

    def __repr__(self):
        return "<TreasuryYear %s>" % self

class Account(models.Model):
    name = models.CharField(max_length=200, help_text='The name of the account', unique=True)

    description = models.TextField()

    @staticmethod
    def get_default():
        try:
            return Account.objects.get(name='Unresolved')
        except Account.DoesNotExist:
            account = Account(name='Unresolved', description='Fake account for unresolved allocations')
            account.save()
            return account

    @property
    def currently_allocated(self):
        return self.allocations.filter(school_year=TreasuryYear.get_current()).aggregate(models.Sum('amount'))['amount__sum'] or 0

    @property
    def currently_free(self):
        return self.balance - self.currently_allocated

    @property
    def balance(self):
        if self.line_items.count() == 0:
            return 0
        return self.line_items.all()[0].balance

    @property
    def bank_amount(self):
        total_pending = self.line_items.filter(check_status=LineItem.PENDING).aggregate(models.Sum('amount'))['amount__sum'] or 0
        return self.balance + total_pending

    def __str__(self):
        return self.name

class Allocation(models.Model):
    def new_allocation_number():
        num =  Allocation.objects.all().aggregate(models.Max('allocation_number'))['allocation_number__max']
        if num is None:
            num = 0
        return num + 1

    allocation_number = models.IntegerField(default=new_allocation_number, unique=True)
    school_year = models.ForeignKey(TreasuryYear, default=TreasuryYear.get_current)
    for_club = models.ForeignKey('Club', blank=True, null=True, related_name='allocations')

    amount = models.DecimalField(decimal_places=2,max_digits=8)
    amount_requested = models.DecimalField(decimal_places=2, max_digits=8, default=0)

    date_approved = models.DateTimeField(null=True, blank=True, help_text='The date the ASHMC council approved this allocation')

    explanation = models.TextField(help_text="Additional stipulations for use of funds or general comments", default="", blank=True)

    source = models.ForeignKey(Account, default=Account.get_default, related_name='allocations')

    @property
    def amount_left(self):
        total_spent = self.allocation_line_items.all().aggregate(models.Sum('amount'))['amount__sum'] or 0
        return self.amount - total_spent

    def __str__(self):
        return 'Allocation %06d' % self.allocation_number

    class Meta:
        ordering = ('allocation_number',)

class Club(models.Model):
    name = models.CharField(max_length=512, unique=True, blank=False, null=False)
    description = models.TextField()

    date_founded = models.DateField(null=True, blank=True)
    date_ended = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('name',)

    @property
    def line_items(self):
        return LineItem.objects.filter(request__club=self)

    @property
    def balance(self):
        spent = self.current_allocations.aggregate(models.Sum('allocation_line_items__amount'))['allocation_line_items__amount__sum'] or 0
        return self.current_allocation - spent

    @property
    def current_allocation(self):
        return self.current_allocations.aggregate(models.Sum('amount'))['amount__sum'] or 0

    @property
    def current_allocations(self):
        return self.allocations.filter(school_year=TreasuryYear.get_current())

    @property
    def current_officers(self):
        return self.officers.filter(school_year=TreasuryYear.get_current())

    @property
    def current_officers_for_allocation(self):
        officers = list(self.officers.filter(school_year=TreasuryYear.get_current())[:5])
        officers += [{'position': '', 'student': ''}] * (5 - len(officers))
        return officers

    def str_id(self):
        return '%06d' % self.id

    def __str__(self):
        return "%s" % (self.name)

    def __repr__(self):
        return "<Club %s>" % self

class Officer(models.Model):
    club = models.ForeignKey('Club', related_name='officers')
    school_year = models.ForeignKey('TreasuryYear', default=TreasuryYear.get_current)

    student = models.ForeignKey('main.Student', related_name='club_positions')
    position = models.CharField(max_length=512, blank=False, null=False)

    main_contact = models.BooleanField(help_text='Whether this officer is the club\'s main contact for the school year')

    is_club_superuser = models.BooleanField(help_text='Whether this officer can access and change this club\'s treasury information', default=True)

    def __str__(self):
        return '%s %s of %s' % (self.school_year, self.position, self.club)

    def __repr__(self):
        return '<%s>' % self

    class Meta:
        unique_together = ('club', 'school_year', 'student') # Ensure each member is listed only once

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

    @staticmethod
    def get_default():
        try:
            return Category.objects.get(name='Miscellaneous')
        except Category.DoesNotExist:
            category = Category(name='Miscellaneous', description='Miscellaneous/Uncategorized items')
            category.save()
            return category

class LineItem(models.Model):
    PENDING = 'Pending'
    RECONCILED = 'Reconciled'

    account = models.ForeignKey('Account', related_name='line_items')
    date_created = models.DateTimeField(auto_now_add=True)

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.CharField(max_length=300)

    check_number = models.IntegerField(help_text='Check number', null=True, blank=True)

    check_status = models.CharField(max_length=100, choices=((PENDING, 'Pending bank approval'),
                                                             (RECONCILED, 'Check cashed')), default=PENDING)

    allocations = models.ManyToManyField('Allocation', related_name='line_items', through='AllocationLineItem')
    request = models.ForeignKey('CheckRequest', null=True, related_name='line_items', blank=True)
    category = models.ForeignKey('Category', null=True, default=Category.get_default)

    def clean(self):
        if self.pk is None:
            self.balance = self.account.balance - self.amount

    @staticmethod
    def post_save(sender, **kwargs):
        self = kwargs['instance']
        total = self.allocation_line_items.all().aggregate(models.Sum('amount'))['amount__sum'] or 0
        if total != self.amount and self.request is not None:
            AllocationLineItem.objects.filter(line_item=self).delete()
            with transaction.commit_on_success():
                # Find allocations based on account source
                allocations = self.request.club.allocations.filter(source=self.account, school_year=TreasuryYear.get_current())
                amount_left = self.amount
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
        ordering = ('-date_created',)

models.signals.post_save.connect(LineItem.post_save, sender=LineItem)

class AllocationLineItem(models.Model):
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


# Create your models here.
class BudgetRequest(models.Model):
    club = models.ForeignKey('Club')
    date_filed = models.DateTimeField(auto_now=True)

    for_school_year = models.ForeignKey('TreasuryYear')

    filer = models.ForeignKey('main.Student')

    mailing_address = models.TextField()

    college = models.CharField(max_length=256)

    attended_budgeting_for = models.CharField('Which budget hearings did you attend last year?', max_length=32,
                                              choices=(('HMC', 'Harvey Mudd College'),
                                                       ('5C', '5C'),
                                                       ('None', 'None')))

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
    internal_fundraising_amount = models.DecimalField(decimal_places=2, max_digits=11)

    # Budget request
    ashmc_amount = models.DecimalField('ASHMC request', decimal_places=2, max_digits=11)
    scripps_amount = models.DecimalField(decimal_places=2, max_digits=11)
    pomona_amount = models.DecimalField(decimal_places=2, max_digits=11)
    cmc_amount = models.DecimalField('CMC amount', decimal_places=2, max_digits=11)
    pitzer_amount = models.DecimalField(decimal_places=2, max_digits=11)
    other_amount = models.DecimalField(decimal_places=2, max_digits=11)
    other_explanation = models.TextField(help_text='Please explain your other source of funding')

    budget_explanation = models.TextField('Please explain why your club deserves funding, or anything else that needs to be made clear')

    approved = models.BooleanField(default=False)
    date_approved = models.DateTimeField(null=False)
    amount_allocated = models.DecimalField(max_digits=11, decimal_places=2)

class BudgetItem(models.Model):
    budget = models.ForeignKey(BudgetRequest)
    item = models.CharField(max_length=512)
    description = models.CharField(max_length=1024)
    amount = models.DecimalField(max_digits=11, decimal_places=2)

class CheckRequest(models.Model):
    REIMBURSEMENT = 'Reimbursement'
    UPFRONT = 'Upfront'
    SEMESTER = 'Semester'
    ENTIRE_YEAR = 'Entire year'

    club = models.ForeignKey(Club, null=True, related_name='check_requests')
    year = models.ForeignKey(TreasuryYear, null=True, default=TreasuryYear.get_current)

    date_filed = models.DateTimeField(auto_now=True)

    filer = models.ForeignKey('main.Student')

    amount = models.DecimalField(max_digits=11, decimal_places=2)

    payee = models.CharField(max_length=512, blank=False)
    deliver_to = models.CharField(max_length=1024, help_text='If different from payee. Include mailbox, if needed', blank=True, null=True)

    request_type = models.CharField(max_length=20, choices=((REIMBURSEMENT, 'Reimbursement for past expenses'),
                                                            (UPFRONT, 'Upfront payment for planned purchase'),
                                                            (SEMESTER, 'Enture allocation for semester'),
                                                            (ENTIRE_YEAR, 'Entire allocation for year')), default=REIMBURSEMENT)

    other_information = models.TextField(help_text='Is there anything else we should know?', blank=True, null=True)

    approved = models.BooleanField(default=False)
    date_approved = models.DateTimeField(null=True, blank=True)
    reason_denied = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-date_filed',)

    def clean(self):
        if self.approved and self.date_approved is None:
            self.date_approved = datetime.datetime.now()

    def __str__(self):
        return 'Check Request for %s on %s (%s)' % (self.club.name, self.date_filed, self.amount)

    @property
    def denied(self):
        return self.date_approved is not None and not self.approved

    @property
    def status(self):
        if self.approved:
            return 'Approved'
        elif self.denied:
            return 'Denied'
        else:
            return 'Pending'
