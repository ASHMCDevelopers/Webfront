# Main

This is the catchall app (as is often found in Django projects), which holds
the basis for all the other apps.

Of particular note is the management command found here:

```
python manage.py get_session_user <session_id>
```

Which will tell you which user was logged in for a given session -- immensely
helpful when trying to debug user-specific issues. It will give you the
primary key, name, and email of the session user.
