"""ITIExamSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from classroom.views import accounting,student,instructor,manager,subject
from django.conf import settings
from django.conf.urls.static import static

handler404 = accounting.handler404

urlpatterns = [
    path('', include('classroom.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/',accounting.SignUpView.as_view() , name='signup'),
    path('accounts/signup/student/', student.StudentSignupView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', instructor.InstructorSignUpView.as_view(), name='instructor_signup'),
    path('accounts/signup/manager/', manager.ManagerSignUpView.as_view(), name='manager_signup'),
    path('accounts/signup/subject/', subject.subject_add, name='subject_add'),
    path('accounts/signup/showInformation/', manager.show_information, name='show_information'),
    path('accounts/signup/showInformation/student/', student.show_information_student, name='show_student_details'),
    path('accounts/signup/showInformation/student/delete/<int:pk>', student.delete_information_student,
         name='delete_student_details'),
    path('accounts/signup/showInformation/instructor/', instructor.show_information_instructor, name='show_instructor_details'),
    path('accounts/signup/showInformation/Instructor/delete/<int:pk>', instructor.delete_information_Instructor, name='delete_Instructor_details'),
    path('accounts/signup/showInformation/subject/', subject.show_information_subject, name='show_subject_details'),
    path('accounts/signup/showInformation/subject/delete/<int:pk>', subject.delete_subject_details, name='delete_subject_details'),
    path('accounts/signup/showInformation/subjectsStudents>', manager.add_subjects_to_students, name='add_subjects_students'),
    path('accounts/signup/student/profile', student.profile, name='student_profile'),
    path('accounts/signup/student/profile/edit', student.edit_profile, name='edit_student_profile'),
    path('accounts/signup/instructor/profile', instructor.profile, name='inst_profile'),
    path('accounts/signup/instructor/profile/edit', instructor.edit_profile, name='edit_instructor_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
