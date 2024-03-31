# Estilo Calico Admin Backend
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"><img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
<img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white">
<img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white">
<img src="https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white">

Custom Cloud-Based Content Management System

Deployed in AWS, React frontend, Python/Flask backend, Terraform for infrastructure as code.

# Running the server
To start flask with hot reloading 

```bash
flask --app app.py --debug run
```

# Testing
The flask app exposes an http API. In order to test this API we need a tool that is capable of making requests with all of the http verbs. Browsers make GET requests when an url is entered into the search bar thus we need a tool that can allow us to test other http verbs (PUT, PATCH, DELETE, POST).

Use Postman for testing http requests. Go to Estilo Calico collection and choose environment to test. To access variables in your environment use {{ VARIABLE NAME }}. Path params are added with a colon (an example is `/:id`). Path variable section will appear in Postman and you can put the corresponding value there. Look at the "Delete event" request for an example. The collection is in account associated with my email. 

Could've chosen curl as well. 

# Date parsing
```python
from dateutil.parser import *
x = parse("Fri, 05 Jan 2024 18:00:00 GMT")
x.strftime("%Y-%m-%dT%H:%M:%SZ")
# -> '2024-01-05T18:00:00Z'
```
When you query using SELECT * FROM events to retrieve events in db psycopg2 returns a datetime object for start_time and start_date when data type for that column is set to timestamp. Didn't need to use dateutil to parse but did use datetime's strftime method to parse datetime object to iso-8601 format.
