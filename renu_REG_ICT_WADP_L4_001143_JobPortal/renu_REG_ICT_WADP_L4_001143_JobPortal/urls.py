from django.contrib import admin
from django.urls import path
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',loginPage,name="loginPage"),
    path('registrationPage/',registrationPage,name="registrationPage"),
    path('profile/',profile,name="profile"),
    path('browsejob/',browsejob,name="browsejob"),
    path('logoutpage/',logoutpage,name="logoutpage"),
    path('editprofile/',editprofile,name="editprofile"),
    
    path('searchpage/',searchpage,name="searchpage"),
    path('appliedjob/',appliedjob,name="appliedjob"),
    path('applicant/<str:myid>',applicant,name="applicant"),
    
    path('applyjob/<str:myid>',applyjob,name="applyjob"),
    path('addjob/',addjob,name="addjob"),
    path('editjob/<str:myid>',editjob,name="editjob"),
    path('deletejob/<str:myid>',deletejob,name="deletejob"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)