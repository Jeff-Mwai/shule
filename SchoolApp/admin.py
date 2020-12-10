from django.contrib import admin

# Register your models here.
from SchoolApp.models import Assignment, Fee

admin.site.register(Assignment)
admin.site.register(Fee)