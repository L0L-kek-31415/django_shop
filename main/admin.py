from django.contrib import admin
from .models import Catalog, Category

admin.site.register([Category, Catalog])
