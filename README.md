# Django Midnight File System
![](https://img.shields.io/badge/Python-3.10.10-blue)
![](https://img.shields.io/badge/Django-4.1.5-%2344B78B)
![](https://img.shields.io/badge/REST%20framework-3.14.0-%23A30000)

Django package that allows to administer in a simple way the resources of an API with Rest Framework using several modes of operation.

## Installation et configuration

### Install python3 

```sh
# ~$
sudo apt install python3;\
sudo apt install python3-pip
```

You have to make sure of the version of python that is installed. The version of python
used is `python 3.10.10`.


### Install venv
You can install a python virtualenv program in two different ways.

```sh
# ~$
sudo apt install python3-venv
```

OR

```sh
# ~$
sudo pip3 install virtualenv
```

### Create virtual environment
In your project root, if you have not already done so, run one of the following commands to create 
a virtual environment.

```sh
# ~$
python3 -m venv env
```

OR

```sh
# ~$
virtualenv env -p python3
```

### Lauch environment

```sh
# ~$
source env/bin/activate
```

### Dependences installation
You must install the following dependences :

```sh
# ~$
pip install -r requirements.txt
```

## Integration
1. Copy `mfs` folder and past it into your root project.
2. Write the following code source in `settings.py` of your Django project.

```python
# ...

# Django guardian settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
)

```

3. In `urls.py` file, write the following code:

```python
# ...

from django.conf import settings
from django.conf.urls.static import static

# ...
# After urlpatterns definition ...

urlpatterns += static(settings.FSURL, document_root=settings.FSDIR);

```

4. Execute the following django commands to make migration of the database File model :

```sh
# ~$
./manage.py makemigrations;\
./manage.py migrate
```

All is done !

## Usage
We will see some examples of use cases in a Django project. Given an application named `galery`.

1. Example 1:
You can create model of image file in `galery` like following code :

```python
from django.utils.translation import gettext_lazy as _
from django.db  import models
from mfs.models import File


```

Now we will try to create an image uploading function in the `views.py` file :

```python
from django.shortcuts import render

from restibm.generics import CreateAPIView
from restibm.viewsets import ModelViewSet

from main.serializers import UserCreateSerializer
from main.serializers import DashboardSerializer
from main.models import User
from main.models import Dashboard


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    model = User
    public = True


class DashboardModelViewSet(ModelViewSet):
    serializer_class = DashboardSerializer
    model = Dashboard

```


