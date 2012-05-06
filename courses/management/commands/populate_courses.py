'''
Created on May 6, 2012

@author: Haak Saxberg
'''
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("populate_from_csv", '.')
        call_command("create_requisites", '.')
        call_command("create_major", 'all')