# perdoo_scheduler

This is a simple scheduler application that allows you to schedule and execute
requests at arbitrary time in the future.

Application is deployed to heroku and available [here](https://ahmet-perdoo.herokuapp.com).

The scheduler runs every minute, picks ups the requests that are to be executed
at that time and performs them. Headers, arguments and body data can be added as
`key:value` entries.


In order to run the app locally:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

In order to simulate the scheduler, you can run it manually as well via Django
management command:
```
python manage.py run_scheduler
```


To run the test suite:
```
DJANGO_SETTINGS_MODULE=config.settings python -m pytest -s scheduler/tests
```

A user account can be created from the UI, and it has `is_staff` flag set to
`True` to be able to access django-admin interface for creation of the 
`RequestSchedule` entries, however the Schedule page will show the listing of
the created requests and their statuses as well.

Enjoy!