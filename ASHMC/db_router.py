'''
Created on Mar 29, 2012

@author: Haak Saxberg
'''
from django.conf import settings
 
CORE_APPS = ('auth', 'django')
 
class DatabaseAppsRouter(object):
    """
    A router to control all database operations on models for different
    databases.
 
    In case an app is not set in settings.DATABASE_APPS_MAPPING, the router
    will fallback to the `default` database.
 
    Settings example:
 
    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}
    """
 
    def db_for_read(self, model, **hints):
        """"Point all read operations to the specific database."""
        #print "R hints: ", hints, " for ", model
        '''if hints.has_key('instance') and settings.DATABASE_APPS_MAPPING.has_key(model._meta.app_label):
            print 'separated app instance'
            try:
                return 'default'
            except Exception, e:
                print e
                return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        '''
        if settings.DATABASE_APPS_MAPPING.has_key(model._meta.app_label):
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None
 
    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""
        #print "W hints: ", hints, " for ", model
        '''if hints.has_key('instance') and settings.DATABASE_APPS_MAPPING.has_key(model._meta.app_label):
            print 'separated app instance'
            try:
                return 'default'
            except Exception, e:
                print e
                return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        '''
        if settings.DATABASE_APPS_MAPPING.has_key(model._meta.app_label):
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None
 
    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        db_obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        db_obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return True
        return None
 
    def allow_syncdb(self, db, model):
        """Make sure that apps only appear in the related database -- except for core apps, which appear everywhere"""
        #if model._meta.app_label in CORE_APPS:
        #    return True
        if db in settings.DATABASE_APPS_MAPPING.values():
            return settings.DATABASE_APPS_MAPPING.get(model._meta.app_label) == db
        elif settings.DATABASE_APPS_MAPPING.has_key(model._meta.app_label):
            return False
        return None