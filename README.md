# MigNow

It's simple project to migrate subscribers data and client data to user object, with validation to avoid data conflicts and collect conflicts data. I called this project MigNow because Mig comes from 'migration' word, Now - comes from simplicity and fast execution.

### How to start ?

* You should install virtualenv and requirements from project root:
    * `sudo pip3 install virtualenv`
    * `virtualenv .venv`
    * `source .venv`
    * `pip3 install -r requirements.txt`

### How to use ?

With enabled virtualenv:
* You should create some objects by using Subscriber, SubscriberSMS, Client, User models.
* You can start using a management commands:
    `python3 manage.py ...:`
  * `migrate_subscribers` - this command migrate subscribers to user models and collect conflicts data.
  * `update_gdpr_consent` - this command update user gdpr_consent field based on subscribers date creation 

### How to run tests ?

With enabled virtualenv:
* You should run command `py.test --cov-report term-missing --cov --flake8`
