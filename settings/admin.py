from django.contrib import admin
from django.apps import apps

app_models = apps.get_models()

# Register all models
for model in app_models:
    if not admin.site.is_registered(model):
        admin.site.register(model)
# Register your models here.
