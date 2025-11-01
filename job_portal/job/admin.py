from django.contrib import admin
from job.models import*
admin.site.register([UserModel,jobModel,employeeModel,applyModel])