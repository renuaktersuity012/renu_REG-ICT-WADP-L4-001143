from django.contrib import admin

# Register your models here.
from django.contrib import admin
from myapp.models import *

# Register your models here.
admin.site.register(JobPortalUser)
admin.site.register(RecruitersModel)
admin.site.register(SeekerModel)
admin.site.register(JobModel)
admin.site.register(jobApplyModel)
