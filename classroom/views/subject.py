from django.views.generic import CreateView
from classroom.models import Subject
from classroom.forms import SubjectAddForm
from django.shortcuts import redirect , render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from classroom.decorators import manager_required
from django.http import JsonResponse

@login_required
@manager_required
def subject_add(request):
    if request.method == 'POST':
        print("============",request.POST)
        subjectForm=SubjectAddForm(request.POST)
        if subjectForm.is_valid():
            subjectForm.save()
            messages.success(request, 'add new subject successfully.......')
            return redirect('subject_add')
        else:
            messages.error(request, 'error in adding new subject .......')
            return redirect('subject_add')
    else:
        return render(request,'registration/signup_form.html',{
            'form':SubjectAddForm ,'user_name': 'Subject'
        })


@login_required
@manager_required
def show_information_subject(request):
    subjects = Subject.objects.all()
    return render(request, 'admin/subject_index.html', {'subjects':subjects})


@login_required
@manager_required
def delete_subject_details(request, pk):
    Subject.objects.get(pk=pk).delete()
    return JsonResponse({"success": True}, status=200)