from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from job.models import*
from django.contrib import messages
def registerPage(request):
    if request.method=="POST":
        fullname=request.POST.get('fullname')
        username=request.POST.get('username')
        role=request.POST.get('role')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        user_exists=UserModel.objects.filter(username=username).exists()
        if user_exists:
            return redirect('registerPage')
        if password==confirm_password:
            user=UserModel.objects.create_user(
                full_name=fullname,
                username=username,
                password=password,
                roles=role
            )
            if role == 'Employee':
                employeeModel.objects.create(employee=user)
            return redirect('loginPage')
    return render(request,'auth/register.html')
def loginPage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('homePage')
    return render(request,'auth/login.html')
def logoutPage(request):
    logout(request)
    return redirect('loginPage')
def changePass(request):
    if request.method=="POST":
        old_password=request.POST.get('old_password')
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')
        if check_password(old_password,request.user.password):
            if new_password==confirm_password:
                request.user.set_password(new_password)
                request.user.save()
            return redirect('loginPage')
    return render(request,'auth/changepass.html')

@login_required
def jobAddPage(request):
    if request.method == "POST":
        Job_title = request.POST.get('Job_title')
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        skills_required = request.POST.get('skills_required')
        salary = request.POST.get('salary')
        application_deadline = request.POST.get('application_deadline')

        employee = employeeModel.objects.get(employee=request.user)

        jobModel.objects.create(
            posted_by=employee,
            Job_title=Job_title,
            company_name=company_name,
            location=location,
            description=description,
            skills_required=skills_required,
            salary=salary,
            application_deadline=application_deadline,
        )
        return redirect('jobPostPage')

    return render(request, 'job/jobAdd.html')
@login_required
def jobPostPage(request):
    query = request.GET.get('q') 
    if request.user.roles == 'Employee':
        employee = employeeModel.objects.get(employee=request.user)
        jobs = jobModel.objects.filter(posted_by=employee)
    else:
        jobs = jobModel.objects.all()
    
    if query:
        jobs = jobs.filter(
            Job_title__icontains=query) or jobs.filter(company_name__icontains=query) or jobs.filter(
            location__icontains=query) or jobs.filter(skills_required__icontains=query)

    return render(request, 'job/jobPost.html', {'jobs': jobs, 'query': query})

def jobEdit(request,id):
    job_data=jobModel.objects.get(id=id)
    if request.method == "POST":
        Job_title = request.POST.get('Job_title')
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        skills_required = request.POST.get('skills_required')
        salary = request.POST.get('salary')
        application_deadline = request.POST.get('application_deadline')
        job_data.Job_title=Job_title
        job_data.company_name=company_name
        job_data.location=location
        job_data.description=description
        job_data.skills_required=skills_required
        job_data.salary=salary
        job_data.application_deadline=application_deadline
        job_data.save()
        return redirect('jobPostPage')
    return render(request,'job/jobEdit.html',{'job_data':job_data})
def jobDlt(request,id):
    jobModel.objects.get(id=id).delete()
    return redirect('jobPostPage')
def Shortlisted(request,id):
    status_data=applyModel.objects.get(id=id)
    if status_data.status == 'Pending':
        status_data.status = 'Shortlisted'
    elif status_data.status == 'Rejected':
        status_data.status = 'Shortlisted'
    status_data.save()
    return redirect('applyList')
def Rejected(request,id):
    status_data=applyModel.objects.get(id=id)
    if status_data.status == 'Pending':
        status_data.status = 'Rejected'
    elif status_data.status == 'Shortlisted':
        status_data.status = 'Rejected'
    status_data.save()
    return redirect('applyList')
@login_required
def applyAdd(request,id):
    if request.method == 'POST':
        cv=request.FILES.get('cv')
        phone_number=request.POST.get('phone_number')
        
        job=jobModel.objects.get(id=id)
        applyModel(
            seeker = request.user ,
            job=job,
            cv=cv,
            phone_number=phone_number,
            status='Pending' 
        ).save()
        return redirect('applyList')
    return render(request,'apply/applyjob.html')
@login_required
def applyList(request):
    if request.user.roles == 'Employee':
        employee = employeeModel.objects.get(employee=request.user)
        apply = applyModel.objects.filter(job__posted_by=employee)
    else:
        apply = applyModel.objects.filter(seeker=request.user)

    return render(request, 'apply/applylist.html', {'apply': apply})

def applyListDlt(request,id):
    applyModel.objects.get(id=id).delete()
    return redirect('applyList')
@login_required
def homePage(request):
    if request.user.roles == 'Employee':
        employee = employeeModel.objects.get(employee=request.user)
        jobs = jobModel.objects.filter(posted_by=employee)
    else:
        jobs = jobModel.objects.all()
        
    query = request.GET.get('q') 
    if query:
        jobs = jobs.filter(
            Job_title__icontains=query) or jobs.filter(company_name__icontains=query) or jobs.filter(
            location__icontains=query) or jobs.filter(skills_required__icontains=query)
    return render (request,'master/base.html',{'jobs':jobs, 'query': query})
def homePage2(request):
    jobs = jobModel.objects.all()
    query = request.GET.get('q') 
    if query:
        jobs = jobs.filter(
            Job_title__icontains=query) or jobs.filter(company_name__icontains=query) or jobs.filter(
            location__icontains=query) or jobs.filter(skills_required__icontains=query)
    
    return render (request,'master/home2.html',{'jobs':jobs, 'query': query})
def notePage(request,id):
    job_data=jobModel.objects.get(id=id)
    if request.method == "POST":
        Job_title = request.POST.get('Job_title')
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        description = request.POST.get('description')
        skills_required = request.POST.get('skills_required')
        salary = request.POST.get('salary')
        application_deadline = request.POST.get('application_deadline')
        job_data.Job_title=Job_title
        job_data.company_name=company_name
        job_data.location=location
        job_data.description=description
        job_data.skills_required=skills_required
        job_data.salary=salary
        job_data.application_deadline=application_deadline
        job_data.save()
        return redirect('jobPostPage')
    return render (request,'job/note.html',{'job_data':job_data})