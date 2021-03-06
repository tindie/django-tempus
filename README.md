# Django Tempus

[![Build Status](https://travis-ci.org/juanriaza/django-tempus.png?branch=master)](https://travis-ci.org/juanriaza/django-tempus)



## Overview

Django Tempus provides url tokens that triggers custom actions.

The flow is:

1. The user requests an url with a token.
2. A middleware decrypt that token and triggers an action.
3. Profit.


## Installation

Install using `pip`, including any optional packages you want...

	$ pip install django-tempus

...or clone the project from github.

    $ git clone git@juanriaza/django-tempus.git
    $ cd django-tempus
    $ pip install -r requirements.txt

## How to use it?

It provides a base middleware, and a template tag. With your own middleware you define the action that is triggered and with the templatetag you create the tokenized urls.

```python
from tempus.middleware import BaseTempusMiddleware


class YourMiddleware(BaseTempusMiddleware):
    param_name = 'tempus'  # you can override the param name
    max_age = None  # you can provide an expiry date (in seconds)

    def success_func(self, request, token_data):
        ...

    def expired_func(self, request, token_data):
        ...
```

Create tokenized urls with the template tag:

```
{% url 'for_something' %}{% tempus {'my_data': 'my_value'} param_name='param_name' %}
```

### Example

We own the `Awesome Shop` where you can find the finest rockets…

![image](http://i.imgur.com/QqH06NS.jpg)

Rockets are pricey… and every single cool pony out there wants one.

We want to boost our sales and we offer a one day discount and mail it to those cute ponies.

Let's go!

```python
from tempus.middleware import BaseTempusMiddleware


class RocketDiscountMiddleware(BaseTempusMiddleware):
    param_name = 'rocket_promo'
    max_age = 86400  # 24h

    def success_func(self, request, token_data):
        discount = token_data.get('discount')
        if discount:
            request.session['discount'] = discount
```

We need to add the `RocketDiscountMiddleware` to `MIDDLEWARE_CLASSES` at `settings.py`

```python
MIDDLEWARE_CLASSES = (
	...
    'awesomeshop.products.middleware.RocketDiscountMiddleware'
)
```

And get the discount:

```python
def rocket_view(request, rocket_model):
	rocket_price = Rocket.objects.get(model=rocket_model).price
	discount = request.session.get('discount', 0)
	rocket_price -= discount
	return render('awesome/template.html', {'price': rocket_price})
```


We're done.

Now we can send special tokenized urls with the discount to our beloved ponies

```
{% load tempus %}

Hi {{ pony_name }},

Just because you rock we offer you a discount on our ultimate X-ROCKET 3K.

{% url 'rocket_url' %}{% tempus {'discount': 500} param_name='rocket_promo' %}
```

![image](http://i.imgur.com/rtAIOCx.png)

## Contrib Packages

### Automatic Login

Add the `tempus.contrib.auto_login.middleware.AutoLoginMiddleware` to `MIDDLEWARE_CLASSES` at `settings.py`

```python
MIDDLEWARE_CLASSES = (
	...
    'tempus.contrib.auto_login.middleware.AutoLoginMiddleware'
)
```

Now we can send emails with urls that logs the user in.

```
{% load tempus %}

Hi {{ pony_name }},

Check your direct messages from {{ another_pony }}.

{% url 'direct_messages' %}{% tempus {'user_pk': user.pk} %}
```


## Running the tests
To run the tests against the current environment:

    $ django-admin.py test tempus --settings=tempus.tests.settings

## Changelog

### 0.2.0

**27th Apr 2013**

* Add compression by default.

### 0.1.0

**17th Feb 2013**

* First release.
