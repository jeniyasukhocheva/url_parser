# Url parser
This is an application for scheduled parsing urls.

### Requirements

This project uses python3 and following libraries:
- Django 2.2.7
- requests
- bs4

To install these libraries run this command: 
```
pip install -r requirements.txt
```

Before running this application you need to run:
```
python manage.py migrate
```

After this create superuser using next command:
```
python manage.py createsuperuser
```

### Running application

To run this application run following command:
```
bash ./run.sh
```

or 
```
python manage.py runserver | python manage.py run_parser
```

This will run a local django server and a parser.  
Go to the admin panel and add urls that you need to be parsed.  
http://127.0.0.1:8000/admin/url_parser/parsertask/

Parsed results will be displayed on the page http://127.0.0.1:8000.
