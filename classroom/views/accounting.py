from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from classroom.decorators import manager_required

@method_decorator([login_required,manager_required] , name='dispatch')
class SignUpView(TemplateView):
    template_name = 'registration/signup.html'



def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('student:exam_list')#student home page
        elif request.user.is_manager:
            return redirect('signup')#manger home page
        else:
            return redirect('instructor:subject_exam_list')#instractor home page
    return  render(request,'classroom/home.html')#home pag



def handler404(request,ex):
    return render(request, '404.html', status=404)

    
def handler500(request,ex):
    return render(request, '500.html', status=500)