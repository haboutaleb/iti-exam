from django.views.generic import CreateView , ListView
from classroom.models import User ,Subject , Question ,Answer , Exam , Student
from classroom.forms import StudentSignupForm ,TakeExamForm
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from classroom.decorators import manager_required,student_required,instructor_required
from classroom.utils import GeneticExam ,Exam as GExam
from django.http import HttpResponse ,JsonResponse


@method_decorator([login_required,manager_required] , name='dispatch')
class StudentSignupView(CreateView):
    model = User
    form_class = StudentSignupForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'add new student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request,'Done! , Add new Student successfully .......')
        return redirect('student_signup')


@method_decorator([login_required,student_required] , name='dispatch')
class SubjectListView(ListView):
    model = Subject
    context_object_name = 'subjects'
    template_name = 'classroom/students/subject_list.html'
    def get_queryset(self):
        queryset = self.request.user.student.subjects.all
        print(queryset)
        return queryset


@login_required
def take_Exam(request,subject_pk):
    subject = get_object_or_404(Subject, pk=subject_pk)
    if  request.user.is_student:
        student = request.user.student
    else:
        student=None
    if request.method == 'POST':
        print(request.POST)
        res = Exam_Result(request.POST.copy())
        if res > 50:
            messages.success(request,f'congrtulations ...... , you passed this exam successfully   your degree : {res}')
        else:
            messages.warning(request,f'oooops , you failed .......  your degree : {res}')
        finalExam = Exam()
        finalExam.subject=subject
        finalExam.student=student
        finalExam.score=res
        finalExam.save()
        return redirect('home')
    else:
        print("========================kkkkkkkkkkkkkkk")
        print(student,subject)
        examnum=Exam.objects.filter(subject=subject,student=student).count()
        print(examnum)
        if  examnum < 0:
            messages.success(request,'you take this subject before .........')
            return redirect("home")
        else:
            ganatic_exam=GeneticExam(subject.pk)
            exam:GExam =ganatic_exam.get_Exam()
            if not exam or not exam.questions:
                messages.warning(request,"please wait , while instructor prepare Exam Questions")
                return redirect('home')
            data=[]
            for i in range(15):
                q=Question.objects.get(pk=exam.questions[i][0])
                answers=Answer.objects.filter(question=q.pk)
                data.append((q , answers))
            return  render(request,'classroom/students/take_quiz_form.html',{
                'data' : data,
                'subject':subject,
                'info':exam.examFitnes
            })




def Exam_Result(Examanswers:dict):
    # {'csrfmiddlewaretoken': ['sdeKFbdiIe3xgJXfxqHPvPU1HvJqpfGomfRgei0OwEzLpazqSWEpPyTMbTD23716'], '129': ['488'],
    #  '23': ['108'], '68': ['284'], '100': ['408'], '32': ['140'], '15': ['76'], '61': ['256'], '97': ['396'],
    #  '4': ['32'], '36': ['156'], '117': ['476'], '44': ['188'], '26': ['116'], '105': ['18'], '78': ['324']}
    del Examanswers['csrfmiddlewaretoken']
    num=0
    for question  in Examanswers:
        a = Answer.objects.get(pk=Examanswers[question])
        if a.is_correct :
            num+=1
        print("qustion" , question)
        print("answers",Examanswers[question])
    return num/15 *100






@method_decorator([login_required,student_required] , name='dispatch')
class TakenExamListView(ListView):
    model = Exam
    context_object_name = 'Exams'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = Exam.objects.filter(student=self.request.user.student)
        print(queryset)
        return queryset


@login_required
@manager_required
def show_information_student(request):
    students = Student.objects.all()
    return render(request, 'admin/student_index.html',{'students':students})


@login_required
@manager_required
def delete_information_student(request,pk):
    User.objects.get(pk=pk).delete()
    return JsonResponse({"success": True}, status=200)


@login_required
@student_required
def profile(request):
    context = {"name":request.user.username,
               "image":request.user.profile_pic.url,
               "country":request.user.country,
               "phone":request.user.phone,
               "birth_date":request.user.birth_date,
               "courses" : request.user.student.subjects.all(),}
    return render(request, "classroom/students/profile.html", context)

@login_required
@student_required
def edit_profile(request):

    if request.method == 'POST':
        print(request.user)
        user = request.user
        user.username = request.POST['name']
        user.birth_date = request.POST['birth_date']
        user.country = request.POST['country']
        user.phone = request.POST['phone']
        if request.FILES:
            user.profile_pic = request.FILES['profile_pic']
        user.save()
        return redirect(reverse("student_profile"))



