# Team Jabiru Small Group project

## Team members
The members of the team are:
- Abbas Bin Vakas
- Arraf Rahman
- Ashley Tyagi
- Jingyi Wang
- Michael Seiranian

## Project structure
The project is called `msms` (Music School Management System).  It currently consists of a single app `lessons` where all functionality resides.

## Deployed version of the application
The deployed version of the application can be found at [Website](https://abbasbinvakas.pythonanywhere.com/).


[Website Admin Dashboard](https://abbasbinvakas.pythonanywhere.com/admin)

SuperUser credentials
- Email: super@super.com
- Password: Password123


## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```


## Sources
The packages used by this application are specified in `requirements.txt`

*Declare other sources here*
