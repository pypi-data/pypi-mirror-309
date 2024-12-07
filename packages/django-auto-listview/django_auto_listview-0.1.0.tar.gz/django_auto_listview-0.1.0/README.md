```markdown
# Django Auto ListView

A Django app to dynamically create `list_display` fields in the admin for all models in your app.

## Installation

You can install `django-auto-listview` either locally (for development purposes) or from PyPI (if it's published).

### Install from PyPI

To install the package from PyPI, run:

```bash
pip install django-auto-listview
```

### Install Locally (For Development)

To install the package locally in development mode (editable install), run:

```bash
pip install -e /path/to/django-auto-listview
```

Replace `/path/to/django-auto-listview` with the path to the `django-auto-listview` directory.

## Usage

After installing the package, follow these steps to integrate it into your Django project.

### 1. Add `django_auto_listview` to `INSTALLED_APPS`

In your `settings.py`, add `django_auto_listview` to the `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    # Other apps
    'django_auto_listview',
    'firstapp',  # Your app (e.g., 'firstapp')
]
```

### 2. Register the Dynamic Admin

In the `admin.py` file of your app (e.g., `firstapp/admin.py`), register the dynamic admin by calling `register_dynamic_admin()`:

```python
from django.contrib import admin
from django_auto_listview.admin import register_dynamic_admin

# Register the dynamic admin for all models in the app
register_dynamic_admin()
```

This will automatically apply the `DynamicModelAdmin` to all models in your app.

### 3. Define Models

Ensure that you have models defined in your app. For example, in `firstapp/models.py`, define a model like this:

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
```

### 4. Run Migrations

After defining your models, run the following commands to create the necessary database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Access the Django Admin

1. Create a superuser if you haven’t already:

    ```bash
    python manage.py createsuperuser
    ```

2. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

3. Visit the Django admin panel at `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

4. You should now see the models (e.g., `Product`) listed in the admin panel. The `DynamicModelAdmin` will dynamically generate `list_display` fields based on the model’s fields, excluding fields that are `blank=True` and `null=False`.

## Customizing the Dynamic Admin

The dynamic admin behavior is based on the fields of your model. If you need to customize how the `list_display` works (e.g., including/excluding certain fields, or altering the display format), you can override the methods of the `DynamicModelAdmin` class.

To customize the behavior, subclass `DynamicModelAdmin` in your `admin.py` file like so:

```python
from django.contrib import admin
from django_auto_listview.admin import DynamicModelAdmin

class CustomProductAdmin(DynamicModelAdmin):
    def get_list_display(self, request):
        # Add custom fields or modify the default behavior
        list_display = super().get_list_display(request)
        list_display.append('price')  # Add 'price' field explicitly
        return list_display

admin.site.register(Product, CustomProductAdmin)
```

This allows you to extend or override any default functionality, such as adding extra fields to the `list_display` or changing how fields are displayed.




