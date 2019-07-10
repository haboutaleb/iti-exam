from django.views.generic import CreateView
from classroom.models import User ,Student,Subject
from django.shortcuts import redirect , render
from django.contrib.auth import login
from classroom.forms import ManagerSignUpForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from classroom.decorators import manager_required
from django.contrib import messages


@method_decorator([login_required,manager_required] , name='dispatch')
class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Signup as a Manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('signup')

@login_required
@manager_required
def add_subjects_to_students(request):
    if request.method== 'POST':
        students=Student.objects.filter(pk__in =request.POST.getlist('students'))
        subjects=Subject.objects.filter(pk__in =request.POST.getlist('subjects'))
        for student in students:
            for subject in subjects:
                student.subjects.add(subject)
                student.save()
        messages.success(request,'subjects were added sucussefly')
        return redirect('home')
    else:
        students=Student.objects.all()
        subjects=Subject.objects.all()
        return render(request,'admin/add_subjects_students.html',{
            'students':students,
            'subjects':subjects
        })

@login_required
@manager_required
def show_information(request):
    return render(request, 'admin/index.html')