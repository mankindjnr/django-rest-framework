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
We will be using the generic views to create our api endpoints.

We will extend the RetrieveAPIView to create a detail view for our product model.

```python
from rest_framework import generics

from .model import Product
from .serializers import ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer # we are serializing the data
```

DetailApiView gets one single item from the database, and we are using the __queryset__ attribute to get all the items from the database.

We will then create a url in product.urls.py file to handle the detail view.

it is a class based view so we will use the __as_view()__ method.
```python
from django.urls import path

from . import views

urlpatterns = [
    path('<int: pk>', views.ProductDetailAPIView.as_view),
]
```
but you can also do this:

```python
product_detail_api_view = ProductDetailAPIView.as_view()

urlpatterns = [
    path('<int: pk>', product_detail_api_view, name='detail'),
]
```

<h2>REST FRAMEWOR CREATE API VIEW</h2>
We will create a create view for our product model.

```python
from rest_framework import generics

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

process_create_view = ProductCreateAPIView.as_view()
```

The purpose of create view is to create a new instance of the model.
It provides a post method to create a new instance of the model - creating a new product.

create.py
```python
import requests

endpoint = "http://127.0.0.1:8000/api/product/"

data = {
    "title": "New Product",
}
resp = requests.post(endpoint, json=data)
print(resp.json())
print(resp.status_code)
```
The above snippet will return a 201 status code, which means the request was successful and a new resource was created.
If the endpoint was called without the __title__ field, it will return a 400 status code, which means the request was not successful. This is because the model requires the __title__ field.

We could also add a function to that class:

```python
def perform_create(self, serializer):
        #serializer.save(user=self.request.user)
        print(serializer.validated_data)
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content") or None
        if content is None:
            content = title
        serializer.save(content=content)
```

<h2>REST FRAMEWORK LIST API VIEW</h2>
We will create a list view for our product model.
A list api view is used to get a list of items from the database, it is read only.
its endpoint represents a collection of model instances i.e products.


```python
from rest_framework import generics

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

process_list_view = ProductListAPIView.as_view()
```

we could also use __ListCreateAPIView__ to create a list and create view at the same time.
This replaces the __ProductCreateAPIView__ and __ProductListAPIView__ classes.

```python
from rest_framework import generics

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

process_list_view = ProductListCreateAPIView.as_view()
```

With the __ListCreateAPIView__ class, we can create a new product and also get a list of all the products.
When you use a __post__ method, you call the _create__ function of it and when you send a __get__ request, you call the __list__ function of it.

***
***
***
<H1>NOT RECOMMENDED</H1>
<h3>USING FUNCTION BASED VIEWS FOR CREATE OR LIST</h3>
We will create a function based view that will handle both the create and list views.

This will kind of mirror the __ListCreateAPIView__ class, the ListCreateAPIView tends to act according to the method used, if its a get request, the it delivers on the list functionality, if its a post mehtod, then it acts on the create functionality.

Also the mehtod get can be used for detail view.

```python

def product_alt_list_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            return product_detail_view(request, pk=pk, *args, **kwargs)
        else:
            return product_list_view(request, *args, **kwargs)

    elif method == "POST":
        return product_create_view(request, *args, **kwargs)
```
***
***
***

<h2>REST FRAMEWORK UPDATE API VIEW</h2>
To update, the method used is __PUT__ and you can only update an existing product

```python
lass ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        #serializer.save(user=self.request.user)
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            #instance.save()

product_update_api_view = ProductUpdateAPIView.as_view()
```
<h4>THE FIELDS</h4>
__queryset__ - this is the queryset of the model you want to update.
__serializer_class__ - this is the serializer class you want to use to serialize the data.
The __lookup_field__ attribute is used to get the instance of the model to be updated.

```python
import requests

endpoint = "http://127.0.0.1:8000/api/product/update/2/"

data = {
    "title": "This is a new title",
    "content": "This is a new content",
    "price": 9400.00
}
resp = requests.put(endpoint, json=data)
print(resp.json())
print(resp.status_code)
```

Here we are passing a new title, new content and a new price as well, the endpoint containes the primary key of the product we will be updating.

We are also passing the updated data as a json object to the endpoint.

<h2>REST FRAMEWORK DELETE API VIEW</h2>
The method used is the __DELETE__ method and you can only delete an existing product.

```python
class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        """if instance is not None:
            return instance.delete()
        return None"""

        super().perform_destroy(instance)

product_destroy_api_view = ProductDestroyAPIView.as_view()

```

delete.py
```python
import requests

endpoint = "http://127.0.0.1:8000/api/product/delete/14/"
resp = requests.delete(endpoint)
print(resp.status_code)
```

<h2>REST FRAMEWORK MIXINS</h2>

***
__RE DO__
***

***

<h2>SESSION AUTHENTICATIONS AND PERMISSIONS</h2>
involves logging the user in and making user they can do only what they are allowed to do.

<h4>permission classes</h4>
if the user is authenticated, allow them to do whatever they want, if they are not authenticated, notify them that they are not authenticated.

```python
from rest_framework import permissions

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
```
With the permission class, goin to the api endpoint, you will get a 403 status code, which means you are not authenticated and therefore forbidden from accessing the resource.

if the permissions class is set:
```python
permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```
then you will be able to access the resource, but you will not be able to make any changes to it.

To solve the not authorized error, you can sue the authorization class.

```python
from rest_framework import permissions, authentication

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
```

I am creating a superuser , logging in to that user and then rerun the listcreateapi view and then i will be able to access the resource. This is because it session based authentication, So as long as i am logged in, i will be able to access the resource.

At this moment i am using the web based interface, but if i use the python client, i will still be unauthorized  since when i run it, it does not log in, hence the session is not created. To create one, you can use selenium. 


<h2>USER AND GROUP PERMISSIONS WIHT DJANGO MODEL PERMISSIONS</h2>
We will be using the django model permissions to create permissions for our users.

After the admin user is created, we are also going to register our models to the admin section to allow us to create groups and permissions. Also allows them to be accessible through the admin section.

Apart from the __admin__ user i created, i have added anotehr user __mannjoro__ who is designated as a __staff__ member.

I have also gone along as the admin, using the admin panel to create a group __staffProductEditor__ with the permission to add, change products. I have also added the __mannjoro__ user to that group. This allows him to have all those permissions given that group.

You can also add permissions directly to the user without having to create a group. click on their name and then add permissions.

```python
    permission_classes = [permissions.DjangoModelPermissions]
```

DjangiModelPermissions allows you to use the django model permissions to control access to the api endpoint.

<h2>CUSTOM PERMISSIONS</h2>


<h2>TOKEN AUTHENTICATION</h2>
We are implementing token authentication to our api endpoints to enable out python client to access the api endpoints.

in our settings.y file, add the following in the installed apps section.

```python
    'rest_framework',
    'rest_framework.authtoken',
```

in out api application urls.py file:
    
```python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/', obtain_auth_token),
]
```
