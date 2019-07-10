from django.views.generic import CreateView ,ListView
from classroom.models import User,Question ,Answer,Subject ,Exam ,Instructor , Student
from classroom.forms import InstructorSignupForm , QuestionForm , BaseAnswerInlineFormSet
from django.contrib import messages
from django.shortcuts import redirect ,render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from classroom.decorators import instructor_required,manager_required
from django.core.paginator import Paginator
from django.db import transaction
from  django.shortcuts import get_object_or_404, reverse
from django.forms import inlineformset_factory
from django.http import JsonResponse , HttpResponse


@method_decorator([login_required,manager_required] , name='dispatch')
class InstructorSignUpView(CreateView):
    model = User
    form_class = InstructorSignupForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type']='add new Instuctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user=form.save()
        messages.success(self.request, 'Done! ,  add new instructor successfully.... ')
        return redirect('instructor_signup')

@method_decorator([login_required,instructor_required],name='dispatch')
class SubjectQustionsView(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'classroom/instructors/question_list.html'

    def get_queryset(self):
        quaryset=Question.objects.filter(subject=(self.request.user.instructor.subject or None))\
            .order_by('id').reverse()
        paginator = Paginator(quaryset, 25)  # Show 25 Question per page
        page = self.request.GET.get('page')
        quaryset = paginator.get_page(page)
        return quaryset


@login_required
@instructor_required
def Question_add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.subject=request.user.instructor.subject
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('instructor:question_answers_add', question.pk)
    else:
        form = QuestionForm()

    return render(request, 'classroom/instructors/question_add_form.html', {'form': form})



@login_required
@instructor_required
def Question_Answers_add(request,question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('instructor:subject_exam_list')

    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    return render(request, 'classroom/instructors/question_change_form.html', {
        'question': question,
        'form': form,
        'formset': formset
    })


@login_required
@instructor_required
def Question_Answers_edit(request,question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.reversesave()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('instructor:subject_exam_list')

    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    return render(request, 'classroom/instructors/question_change_form.html', {
        'question': question,
        'form': form,
        'formset': formset
    })


@login_required
@instructor_required
def Question_Answers_delete(request, question_pk):
    if request.method == 'GET':
        Question.objects.filter(id=question_pk).delete()
        return JsonResponse({"success": True}, status=200)
    else:
        return HttpResponse ("Error in deleteing")




@login_required
@instructor_required
def set_subject_Exam_degree(request):
    subject= Subject.objects.get(instructor=request.user.instructor)
    if 1 < int(request.POST['difficult_num']) <= 14 \
        and 3 < (int(request.POST['ramining_num']) + \
            int(request.POST['understanding_num'])) <15 :
        subject.question_num_difficult=request.POST['difficult_num']
        subject.question_num_ramining=request.POST['ramining_num']
        subject.question_num_understanding=request.POST['understanding_num']
        subject.save()
        messages.success(request,"subject level updated")
    else:
        messages.warning(request, ' please , make sure number of questions is 15!!!!' )
    return redirect('instructor:subject_exam_list')



@method_decorator([login_required,instructor_required] , name='dispatch')
class TakenExamListView(ListView):
    model = Exam
    context_object_name = 'Exams'
    template_name = 'classroom/instructors/taken_quiz_list.html'

    def get_queryset(self):
        queryset = Exam.objects.filter(subject=self.request.user.instructor.subject)
        print(queryset)
        return queryset



@login_required
@instructor_required
def showStudents(request):
    students=request.user.instructor.subject.students.all()
    return render(request,'classroom/instructors/students_list.html',{'students':students})


@login_required
@instructor_required
def showStudentExams(request,student_pk):
    studentExams=Exam.objects.filter(student=student_pk)
    return render(request,'classroom/instructors/taken_quiz_list.html',{'Exams':studentExams})






@login_required
@manager_required
def show_information_instructor(request):
    Instructors = Instructor.objects.all()
    return render(request, 'admin/instructor_index.html',{'Instructors':Instructors})


@login_required
@manager_required
def delete_information_Instructor(request, pk):
    User.objects.get(pk=pk).delete()
    return JsonResponse({"success": True}, status=200)


@login_required
@instructor_required
def profile(request):
    context = {"name": request.user.username,
               "image": request.user.profile_pic.url,
               "country": request.user.country,
               "phone": request.user.phone,
               "birth_date": request.user.birth_date,
               "course" : request.user.instructor.subject,}
    return render(request, "classroom/students/profile.html", context)

@login_required
@instructor_required
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
        return redirect(reverse("inst_profile"))