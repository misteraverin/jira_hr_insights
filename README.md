# Spring Hach: Gazprom case

## Usage

Here are some quickstart instructions, although I would look at the [documentation](https://github.com/tko22/flask-boilerplate/wiki) for more details and other options of setting up your environment (e.g. full Docker setup, installed postgres instance, pipenv, etc).

First start a postgres docker container and persist the data with a volume `flask-app-db`:

```
make start_dev_db
```

Another option is to create a postgres instance on a cloud service like elephantsql and connect it to this app. Remember to change the postgres url and don't hard code it in!

Then, start your virtual environment

```
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate
```
Now, install the python dependencies and run the server:
```
(venv) $ pip install -r requirements.txt
(venv) $ pip install -r requirements-dev.txt
(venv) $ python manage.py recreate_db
(venv) $ python manage.py runserver
```

To exit the virtual environment:
```
(venv) $ deactivate
$
```

For ease of setup, I have hard-coded postgres URLs for development and docker configurations. If you are using a separate postgres instance as mentioned above, _do not hardcode_ the postgres url including the credentials to your code. Instead, create a file called `creds.ini` in the same directory level as `manage.py` and write something like this:

```
[pg_creds]
pg_url = postgresql://testusr:password@127.0.0.1:5432/testdb
```
Note: you will need to call `api.core.get_pg_url` in the Config file.

For production, you should do something similar with the flask `SECRET_KEY`.

#### Easier setup

I've created a makefile to make this entire process easier but purposely provided verbose instructions there to show you what is necessary to start this application. To do so:
```
$ make setup
```

If you like to destroy your docker postgres database and start over, run:
```
$ make recreate_db
```
This is under the assumption that you have only set up one postgres container that's linked to the `flask-app-db` volume.

I would highly suggest reading the [documentation](https://github.com/tko22/flask-boilerplate/wiki) for more details on setup.
