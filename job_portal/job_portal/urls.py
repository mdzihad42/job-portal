
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from job.views import*
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homePage2,name='homePage2'),
    path('homePage/',homePage,name='homePage'),
    path('registerPage/',registerPage,name='registerPage'),
    path('loginPage/',loginPage,name='loginPage'),
    path('logoutPage/',logoutPage,name='logoutPage'),
    path('changePass/',changePass,name='changePass'),
    path('jobAddPage/',jobAddPage,name='jobAddPage'),
    path('jobPostPage/',jobPostPage,name='jobPostPage'),
    
     path('notePage/<int:id>',notePage,name='notePage'),
    
    path('applyListDlt/<int:id>',applyListDlt,name='applyListDlt'),
    
    path('jobEdit/<int:id>',jobEdit,name='jobEdit'),
    path('jobDlt/<int:id>',jobDlt,name='jobDlt'),
    
    path('applyAdd/<int:id>',applyAdd,name='applyAdd'),
    path('applyList/',applyList,name='applyList'),
    
    path('Shortlisted/<int:id>',Shortlisted,name='Shortlisted'),
    path('Rejected/<int:id>',Rejected,name='Rejected'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
