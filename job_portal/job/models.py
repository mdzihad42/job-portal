from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    ROLES=[
        ('Employee','Employee'),
        ('Job_Seeker','Job_Seeker'),
    ]
    full_name=models.CharField(max_length=100,null=True)
    roles=models.CharField(choices=ROLES, max_length=100,null=True)
    
    def __str__(self):
        return self.username
    
class employeeModel(models.Model):
    employee=models.OneToOneField(UserModel, null=True, on_delete=models.CASCADE,related_name='employee_info')
    phone_number=models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.employee.full_name
    
class  jobModel(models.Model):
    posted_by=models.ForeignKey(employeeModel,null=True, on_delete=models.CASCADE)
    Job_title=models.CharField(max_length=100,null=True)
    company_name=models.CharField(max_length=100,null=True)
    location=models.CharField(max_length=300,null=True)
    description=models.TextField(null=True)
    skills_required=models.CharField(max_length=200,null=True)
    salary=models.CharField(max_length=100,null=True)
    application_deadline=models.DateField(null=True)
    
    def __str__(self):
        return self.posted_by.employee.full_name
    
class applyModel(models.Model):
    status=[
        ('Shortlisted','Shortlisted'),
        ('Rejected','Rejected'),
    ]
    seeker=models.ForeignKey(UserModel,null=True, on_delete=models.CASCADE)
    job=models.ForeignKey(jobModel,null=True, on_delete=models.CASCADE)
    cv=models.FileField(null=True,upload_to='job/cv')
    phone_number=models.CharField(max_length=30,null=True)
    status=models.CharField(choices=status, max_length=100,null=True)
    
    def __str__(self):
        return self.seeker.full_name