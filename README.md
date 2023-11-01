<h1>DJANGO REST FRAMEWORK</h1>
We will have two folders 

<h2>1. Backend</h2>
This is where our django project will live and the djnago rest framework.

<h2>2. py_client</h2>
This will then consume that backend.

<h3>BACKEND</h3>
Cd to the folder and start a djnago project
```python
django-admin startproject cfehome
```

<h3>CREATING A PY_CLIENT</h3>

```python
import requests

endpoint = "https://httpbin.org/"

# GET
resp = requests.get(endpoint)
print(resp.text)
```
Running the above snippet gives you the raw html code for that page, this is because its a regular http get request. (A non-Api requests) - Thats why its response is in html.

An API request is a request that is made to a server that is expecting a response in a specific format. (JSON, XML, etc)

```python
import requests

endpoint = "https://httpbin.org/anything"
resp = requests.get(endpoint)
print(resp.text)
print(resp.json())
```

The above snippet will give you a json response. The json() method will convert the response to a python dictionary.

basic.py
```python
import requests

endpoint = "http://127.0.0.1:8000/"
resp = requests.get(endpoint)
print(resp.text)
```
This  snippet is accesing the django project we created earlier through its development server.
Since we have not built anything, we will access the raw text only, not the json response.

<h3>CREATING OUR FIRST API VIEW</h3>
```python
python manage.py startapp api
```

inside  the api folder, create a file called views.py
```python
from django.http import JsonResponse

def home_view(request, *args, **kwargs):
    return JsonResponse({"name": "John", "age": 36})
```

We can now query this using our basic.py file
```python
import requests

endpoint = "http://127.0.0.1:8000/api/"
resp = requests.get(endpoint)
```

<h3>ECHO GET DATA</h3>
on the snippet above we just worked with raw data and we want to work with data that we send to the server. Interaction with the database.

In this section we will replicate the functionality of the httpbin.org/anything endpoint. We will send data to the server and the server will echo it back to us.

```python
def api_echo(request, *args, **kwargs):
    body = request.body # byte string of json data

    data = {}

    try:
        data = json.loads(body)
    except:
        pass
    print(data.keys())
    return JsonResponse(data)
```

on the snippet above, we are relying on the __request__ argument passed to the api_echo function by django. Whwn that view is called, the __request__ argumnet contains all the data sent to that view. We extract that data using the __request.body__ attribute. This is a byte string of the data sent to the server. We then convert that byte string to a python dictionary using the __json.loads()__ method.

```python
data = json.loads(body)
```

with the data now, we can extract the key ```data.keys()``` or we can do whatever we want with it. In this case, we will just return it back to the user.

We are using the try and except block because its not always that your request has a body, we are expecting something like
```python
requests.get(endpoint, params={"name": "John", "age": 36}, json={"query": "hello john"})
```
but you might send a request like
```python
requests.get(endpoint)
```

so instead of getting an error, we will get an empty dictionary.

We can also pass more info to the data we are sending back to the user.

```bash
endpoint = "http://127.0.0.1:8000/api/"
resp = requests.get(endpoint, params={"njoro": 940}, json={'content': 'test the world'})
print(resp.json())
```

```python
def api_echo(request, *args, **kwargs):
    body = request.body # byte string of json data

    data = {}

    try:
        data = json.loads(body)
    except:
        pass

    # addind more data to the data dictionary data
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type
    return JsonResponse(data)


{'content': 'test the world', 'headers': {'Content-Length': '29', 'Content-Type': 'application/json', 'Host': '127.0.0.1:8000', 'User-Agent': 'python-requests/2.31.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}, 'content_type': 'application/json'}
```

__request.headers__ is not json serializable, so we convert it to a dictionary using the __dict()__ method.

We also want to echo the params a.k.a(query_parameters) we are sending to the server.
In a url, they are passed as key value pairs after the question mark. ```?key=value```

we acan set them directly to the url ``` https://httpbin.org/anything?name=john&age=36``` or you could pass them as a dictionary to the __params__ argument of the __requests.get()__ method. ``` requests.get(endpoint, params={"name": "John", "age": 36})```


### ACCESSING QUERY PARAMETERS

```python
request.GET
```
This is a dictionary of all the query parameters sent to the server. We can access them using the __request.GET.get()__ method.

***

At the moment, we are manually enforcing some elements to dictionary format but this is not reliable since not all data can be converted.
To resolve this issue, we turn to django models, we will no longer just echo the data back to the user, we will save it to the database.

***

<h1>DJANGO MODEL INSTANCE AS AN API RESPONSE</h1>
We will create a django model and respond on our api_home view with an instance of that model.

For this we are creating another app __product__

We create a django model in the __product__ app
After migrating our changes, we then open our django python shell and create an instance of the model.

```bash
python manage.py shell
```

We then add data to the model

```shell
from product.models import Product

Product.objects.create(title="New ", description="Awesome product", price=9.49)
Product.objects.create(title="New Product", description="Awesome ", price=9.59)
Product.objects.create(title=" Product", description=" product", price=9.99)
```

To get a random product, we use the __order_by__ method and pass it a question mark. This will return a random product.

```shell
Product.objects.all().order_by("?").first()
```

To query that model as an api endpoint, you can create a view in the product app, but we will stick to the api app views.py file.

```python
from product.models import Product

def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    data = {}

    if model_data:
        data = {
            "id": model_data.id,
            "title": model_data.title,
            "content": model_data.content,
            "price": model_data.price
        }
    return JsonResponse(data)
```

Here we are just returning a random product from the database. We are not using the __request__ argument passed to the function, and the endpoint.

The method we have used above is not the best way to do it, we will use django serializers.

__we will get the model instance, convert it to a python dictionary and then pass it to the JsonResponse() method and return it to our client__


<h2>DJANGO MODEL INSTANCE TO DICTIONARY</h2>
We will use the __model_to_dict()__ method from the django.forms.models module.

```python
from django.forms.models import model_to_dict

def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    data = {}

    if model_data:
        data = model_to_dict(model_data)
    return JsonResponse(data)
```
while converting to the model_to_dict you can also specify the fields you want to convert and then that api will respond with only those fields.

```python
from django.forms.models import model_to_dict

data = model_to_dict(model_data, fields=["title", "price"])
```

<h2>REST FRAMEWORK VIEW AND RESPONSE</h2>
If you want to  run the rest view in browser, after installing the django rest framework, you will have to add the rest framework to the installed apps in the settings.py file.

We will be converting our api_home view to a rest framework view.

```python
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    data = {}

    if model_data:
        data = model_to_dict(model_data)
    return Response(data)
```

With a rest framework view, you have to set the allowed methods in the __api_view__ decorator. This is because rest framework views are not like django views, they are not class based views, they are function based views.

Earlief when we used the pure django view, we used the model_to_dict method, with a rest framework view, we will use a serializer.

<h2>DJANGO EST FRAMEWORK  MODEL SERIALIZER</h2>
(serializers.py)

we have added a __@property__ in our model to get the __sale_price__ of the product.

```python
@property
def sale_price(self):
    return self.price - 1
```

But when we create an instance of the model, the __sale_price__ is not included in the response.
To include it, we will create a serializer for the model.

```python
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'content',
            'price',
            'sale_price'
        ]
```
This way, when we are creating and instance of the model and then serializing it, the __sale_price__ will be included in the response.

```python
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.serializers import ProductSerializer

@api_view(['GET'])
def api_home(request, *args, **kwargs):
    instance = Product.objects.all().order_by("?").first()
    data = {}

    if model_data:
        serializer = ProductSerializer(instance)
        data = serializer.data
    return Response(data)
```

Serializers are also great when it comes to enriching with other values.
i.e we may want to have an instance mehtod __get_discount__ that returns the __discount__ of the product

```python
def get_discount(self):
    return self.price * 0.5
```

then in the serializer.py we can add a field that will return the __discount__ of the product and if we don't want what is want a different name other that __get_discount__ we can:

```python
discount = serializers.SerializerMethodField(read_only=True)

class Meta:
    model = Product
    fields = [
        'id',
        'title',
        'content',
        'price',
        'sale_price',
        'discount'
    ]

def get_discount(self, obj):
    return obj.get_discount()

```

Above, discount is a field in the serializer, and we are using the __get_discount__ method to get the value of the field. Now when returned, the response will have a __discount__ field.

***
So far we have worked with the get method, we will now work with the post method. Here we will also use a serializer and this time the serializer can clean the data for us.

<h2>POST DATA WITH DJANGO REST FRAMEWORK VIEWS</h2>
client.py

```python
import requests

endpoint = "http://127.0.0.1:8000/api/"
resp = requests.post(endpoint, params={"NJORO": 940}, json={"title": "hellow mankind"})
print(resp.status_code)
```

We are sending a post request to the api endpoint, with a query parameter and a json data.

```python
@api_view(['POST'])
def api_home(request, *args, **kwargs):
    data = request.data
    return Response(data)
```
What we also want is to send the data through the serializer, this way, it is validated first before being saved to the database.

```python
@api_view(['POST'])
def api_home(request, *args, **kwargs):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        print(serializer.data)
        return Response(serializer.data)
```
Serializer checks if teh data passes the requirements of the fields in the model, if it does, it saves it to the database and returns the data. It also does check if the data meets the fields of the serializer.

You can also add a roubust error message to the api by setting the raise_exception to True.
```python
if serializer.is_valid(raise_exception=True):
    instance = serializer.save()
    print(serializer.data)
    return Response(serializer.data)

return Response({"errors": serializer.errors}, status=400)
```

<h2>REST FRAMEWORK GENERIC VIEWS</h2>
