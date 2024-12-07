from django.contrib import admin
from django.apps import apps

class DynamicModelAdmin(admin.ModelAdmin):
    # Dynamically generate the list_display excluding fields with blank=True and null=False
    def get_list_display(self, request):
        list_display = [
            field.name for field in self.model._meta.fields
            if not (field.get_internal_type() in ['ManyToManyField', 'TextField', 'ImageField', 'FileField'] or 
                    (field.blank and not field.null))
        ]
        return list_display

    # Customize how fields are displayed in the list view
    def display_field(self, obj, field_name):
        value = getattr(obj, field_name)
        return str(value) if value is not None else 'NULL'

    # Method to dynamically add display methods for each field
    def add_field_display_methods(self):
        for field in self.model._meta.fields:
            if not (field.get_internal_type() in ['ManyToManyField', 'TextField', 'ImageField', 'FileField'] or 
                    (field.blank and not field.null)):
                # Create a method for each field to handle the display
                setattr(self.__class__, field.name, 
                        lambda obj, field_name=field.name: self.display_field(obj, field_name))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.add_field_display_methods()  # Call to add display methods
        return qs


from django.contrib.auth.models import User, Group

def register_dynamic_admin():
    # List of models to exclude from dynamic registration
    excluded_models = [User, Group]
    
    # Automatically register all models in the app, except the excluded ones
    for model in apps.get_models():
        if model not in excluded_models:
            # Register the model only if it isn't in the excluded list
            admin.site.register(model, DynamicModelAdmin)
