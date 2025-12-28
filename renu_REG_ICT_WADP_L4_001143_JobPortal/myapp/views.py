from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from .forms import *

# Create your views here.
def registrationPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        displayname = request.POST.get('displayname')
        email = request.POST.get('email')
        usertype = request.POST.get('usertype')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            user = JobPortalUser.objects.create_user(
                username = username,
                DisplayName=displayname,
                email=email,
                UserType=usertype,
                password = password, 
            )
            user.save()
            if usertype == 'Recruiters':
                recrcreate = RecruitersModel.objects.create(jobuser = user)
                recrcreate.save()
            else:
                seekercreate = SeekerModel.objects.create(jobuser = user)
                seekercreate.save()
            return redirect('loginPage')
    
    return render(request,'signup.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect('profile')
    return render(request,'signin.html')

@login_required
def logoutpage(request):
    logout(request)
    return redirect('loginPage')

@login_required
def profile(request):
    
    return render(request,'profile.html')

@login_required
def addjob(request):
    current_user = request.user
    if request.method == 'POST':
        jobform = JobForm(request.POST)
        if jobform.is_valid():
            job = jobform.save(commit=False)
            job.Created_By = current_user
            job.save()
            return redirect('browsejob')
    else:
        jobform = JobForm()
    context = {
        'jobform':jobform,
    }
    return render(request,'addjob.html',context)

@login_required
def browsejob(request):
    current_user= request.user
    usertype = request.user.UserType
    if usertype == 'Recruiters':
        jobdata= JobModel.objects.filter(Created_By=current_user)
    else:
        jobdata= JobModel.objects.all()
    
    context = {
        'jobdata':jobdata
    }
    
    return render(request, 'browsejob.html',context)


@login_required
def editjob(request, myid):
    
    jobdata = get_object_or_404(JobModel, id=myid)
    if request.method == 'POST':
        jobform = JobForm(request.POST, request.FILES,instance=jobdata)
        
        if jobform.is_valid():
            jobdata = jobform.save(commit=False)
            jobdata.CreatedBy = request.user
            jobdata.save()
            return redirect('browsejob')
    else:
        jobform = JobForm(instance=jobdata)
    
    context = {
        'jobform':jobform
    }
    
    return render(request, 'editjob.html',context)

@login_required
def deletejob(request, myid):
    jobdata = get_object_or_404(JobModel, id=myid)
    jobdata.delete()
    return redirect('browsejob')

@login_required
def postedjob(request):
    current_user = request.user
    current_usertype =request.user.UserType
    
    if current_usertype == 'Recruiter':
        jobdata = JobModel.objects.filter(CreatedBy=current_user)
    else:
        jobdata = JobModel.objects.all()
    
    context = {
        'jobdata':jobdata
    }
        
    
    return render(request,'postedjob.html',context)

@login_required
def editprofile(request):
    current_usertype = request.user.UserType
    userdata = get_object_or_404(JobPortalUser, username=request.user)
    if current_usertype == 'Recruiters':
        recruiterdata = get_object_or_404(RecruitersModel, jobuser = request.user)
        if request.method == 'POST':
            userform = UserForm(request.POST, instance=userdata)
            recruiterform = RecruitersForm(request.POST, request.FILES,instance=recruiterdata)
            
            if userform.is_valid() and recruiterform.is_valid():
                userform.save()
                recruiterform.save()
                return redirect('profile')
        else:
            userform = UserForm(instance=userdata)
            recruiterform = RecruitersForm(instance=recruiterdata)
        context = {
                'userform':userform,
                'recruiterform':recruiterform,
            }
    elif current_usertype == 'Jobseekers':
        seekerdata = get_object_or_404(SeekerModel, jobuser = request.user)
        if request.method == 'POST':
            userform = UserForm(request.POST, instance=userdata)
            seekerform = SeekerForm(request.POST, request.FILES,instance=seekerdata)
            
            if userform.is_valid() and seekerform.is_valid():
                userform.save()
                seekerform.save()
                return redirect('profile')
        else:
            userform = UserForm(instance=userdata)
            seekerform = SeekerForm(instance=seekerdata)
    
        context = {
            'userform':userform,
            'seekerform':seekerform,
        }
    
    return render(request,'editprofile.html',context)



def searchpage(request):
    
    # search option 
    search=request.GET.get('search')
    jobs = JobModel.objects.filter(
        Q(Skills_Set__icontains=search)|
        Q(Title__icontains=search)
        )
    jobDict={
        'job_filtered':jobs
    }
    return render(request,'search.html',jobDict)

@login_required
def applyjob(request,myid):
    jobdata = get_object_or_404(JobModel,id = myid)
    userdata = get_object_or_404(JobPortalUser, username = request.user)
    
    jobapply = jobApplyModel.objects.create(applicant=userdata,job=jobdata)
    
    
    return redirect('appliedjob')
    
    
    
def appliedjob(request):
    current_user= request.user

    jobdata= jobApplyModel.objects.filter(applicant=current_user)

    context = {
        'jobdata':jobdata
    }
    
    return render(request,'appliedjob.html',context)


def applicant(request,myid):
    
    jobdata = get_object_or_404(JobModel, id=myid)
    applicant = jobApplyModel.objects.filter(job=jobdata)
    
    context = {
        'jobdata':jobdata,
        'applicant': applicant,
    }
    
    return render(request,'applicant.html',context)
