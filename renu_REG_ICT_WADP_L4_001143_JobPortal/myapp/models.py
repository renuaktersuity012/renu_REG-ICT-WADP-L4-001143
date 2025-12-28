from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class JobPortalUser(AbstractUser):
    DisplayName = models.CharField(max_length=100,null=True)
    USERTYPE = [
        ('Recruiters','Recruiters'),
        ('Jobseekers','Jobseekers'),
    ]
    UserType = models.CharField(choices=USERTYPE,max_length=100,null=True)
    pass
class RecruitersModel(models.Model):
    jobuser = models.OneToOneField(JobPortalUser,on_delete=models.CASCADE,related_name='recruitermodel',null=True)
    CompanyName = models.CharField(max_length=100,null=True)
    CompanyAddress = models.CharField(max_length=100,null=True)
    CompanyLogo = models.ImageField(upload_to='media/logo/',null=True)
 
class SeekerModel(models.Model):
    jobuser = models.OneToOneField(JobPortalUser,on_delete=models.CASCADE,related_name='seekermodel',null=True)
    SkillsSet = models.TextField(null=True)
    Resume = models.FileField(upload_to='media/resume/',null=True)
    
class JobModel(models.Model):
    Title = models.CharField(max_length=100,null=True)
    Number_Of_Openings = models.CharField(max_length=50,null=True)
    Category = models.CharField(max_length=50,null=True)
    Job_Description = models.TextField(null=True)
    Skills_Set = models.TextField(null=True)
    Created_By = models.ForeignKey(JobPortalUser,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.Title
    
class jobApplyModel(models.Model):
    applicant = models.ForeignKey(JobPortalUser,on_delete=models.CASCADE, related_name='applicantuser', null=True)
    job = models.ForeignKey(JobModel,on_delete=models.CASCADE, related_name='jobapply', null=True)
    status= models.CharField(max_length=100,default="Pending", null=True)
    
    def __str__(self):
        return self.applicant.username