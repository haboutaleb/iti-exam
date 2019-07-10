from django.contrib.auth.forms import UserCreationForm
from classroom.models import User , Question ,Answer,StudentAnswer
from django import forms
from classroom.models import Subject
from django.db import transaction
from classroom.models import (Student , Instructor)
from django.core.validators import ValidationError





class StudentSignupForm(UserCreationForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_student=True
        user.save()
        student = Student.objects.create(user=user)
        student.subjects.add(*self.cleaned_data.get('subjects'))
        return user


class StudentSubjectsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('subjects',)
        widgets = {
            'subjects' : forms.CheckboxSelectMultiple
        }



class InstructorSignupForm(UserCreationForm):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(instructor=None),
        empty_label="----------",
        required=True,
        initial=None,
        label=None
    )
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save()
        user.is_instructor = True
        print("+++++++++++++++")
        user.save()
        print(user)
        teacher = Instructor.objects.create(user=user,subject=self.cleaned_data.get('subject'))
     -   return user


class ManagerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        if commit:
            user.save()
        return user



class SubjectAddForm(forms.ModelForm):
    name =forms.CharField(max_length=50,required=True)
    color=forms.CharField(max_length=7,required=False)
    class Meta:
        model = Subject
        fields = ['name','color',]




class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text','difficulty','objective','chapter_num')



class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeExamForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')




