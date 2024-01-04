# Running the server
To start flask with hot reloading 

```bash
flask --app app.py --debug run
```

# Testing
The flask app exposes an http API. In order to test this API we need a tool that is capable of making requests with all of the http verbs. Browsers make GET requests when an url is entered into the search bar thus we need a tool that can allow us to test other http verbs (PUT, PATCH, DELETE, POST).

Use Postman for testing http requests. Go to Estilo Calico collection and choose environment to test. To access variables in your environment use {{ VARIABLE NAME }}. Path params are added with a colon (an example is `/:id`). Path variable section will appear in Postman and you can put the corresponding value there. Look at the "Delete event" request for an example. The collection is in account associated with my email. 

Could've chosen curl as well. 

