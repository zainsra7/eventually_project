# Eventually
Web application for hosting, sharing and joining local events at the University of Glasgow.

#### Demonstration YouTube Video: https://youtu.be/H4MuH3j7ynQ
#### Pythonanywhere Demo: http://eventually.pythonanywhere.com/


### Setup Email

According to SendGrid, username and password details cannot be uploaded to a public repository, so in order for email to work, please include following
username and password in the "eventually_project/settings.py":

```
EMAIL_HOST_USER = '' # Insert the github username of the owner of this repository


EMAIL_HOST_PASSWORD = 'eventually1234'
```

### Setup and Run Project

1. Clone Repo
2. Create virtual Environment
3. Makemigrations
4. Migrate. If "No Such Table" error occurs, then execute following command:
        ```
        python manage.py migrate --run-syncdb
        ```
5. Run population_script.py
6. (For Admin) -> createsuperuser
7. View population_script.py for username and password
