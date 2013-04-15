# Roster

This package knows where students live in the school and what year they are,
so that the rest of the system can correctly show relevant voting options,
news posts, events, etc.

Currently there's not a lot of exciting things in here, but this app does define
one important management command: `scrape_roster`.

The `scrape_roster` command loads up an excel file (whose columns are defined in
your `local_settings` module), and parses it for new students, changed room
assignments, and also notes any students who don't appear on it anymore.

This only assigns rooms on a semesterly-basis. If you spell out the all the
commands defaults, it would look like this:

```
python manage.py scrape_roster
   --semester-code=FA
   --year=<current year>

   <path/to/excel/file>
```
