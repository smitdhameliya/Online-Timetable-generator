"""timetable_final1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^(?!/?static/)(?!/?media/)(?P<path>.*\..*)$',
        RedirectView.as_view(url='static/%(path)s', permanent=False)),
        
    url(r'^timetable_gen/',views.timetable_gen2,name="timetable generation"),
    url(r'^faculty/delete/', views.faculty_delete,name="faculty_delete"),
    url(r'^faculty/update/', views.faculty_update,name="faculty_update"),
    # url(r'^discipline1/', views.subject1,name="one subject"),
    url(r'^faculty_pref/', views.faculty_preference,name="faculty_preference"),
    url(r'^disciplinelist/', views.discipline_list,name='disciplinelist'),
    url(r'^gettimetable/', views.timetable_gen2,name='timetable_gen'),
    url(r'^fetch/', views.fetch,name='fetch timetable'),
    url(r'^subject/delete/',views.delete_subject,name='subject_delete'),
    url(r'^subject/update/',views.sub_update,name='subject_delete'),
    url(r'^subject/',csrf_exempt(views.Subject.as_view()),name='subject'),
    url(r'^faculty_view/',views.faculty_view,name='faculty_view'),
    url(r'^faculty/', csrf_exempt(views.Faculty.as_view()),name="faculty"),
    url(r'^login/',views.login_view,name="login"),
    url(r'^register/',views.register_view,name="register_view"),
    url(r'^single_faculty/',views.single_faculty,name="register_view"),
    url(r'^getAllSubjects/', views.subjects,name="subjects"),
    # url(r'^faculty/', csrf_exempt(views.Faculty_Login.as_view()),name="faculty_login"),


    # static files (*.styles, *.js, *.jpg etc.) served on /
    # (assuming Django uses /static/ and /media/ for static/media urls)




    url(r'^', RedirectView.as_view(url="static/index.html")),
]
