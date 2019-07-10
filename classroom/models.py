
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator,ValidationError
from django.utils.html import escape,mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, null=True)
    country = models.CharField(default='Egypt', blank=True, null=True, max_length=50)
    birth_date = models.DateField(null=True)
    profile_pic = models.ImageField(upload_to="profile_pics", default="profile_pics/default.jpg")

class Subject(models.Model):
    name=models.CharField(max_length=50 , unique = True)
    color = models.CharField(max_length=7,default='#007bff')
    value = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0.3), MaxValueValidator(0.8)]
    )
    question_num_difficult=models.IntegerField(
        default=1
    )
    question_num_understanding=models.IntegerField(
        default=1
    )
    question_num_ramining=models.IntegerField(
        default=1
    )
    chapter_num=models.IntegerField(
        default=1
    )




    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    subjects = models.ManyToManyField(Subject,related_name='students')

    def __str__(self):
        return self.user.username

class Instructor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    subject = models.OneToOneField(Subject,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    text=models.CharField('Question',max_length=255)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='questions')
    value = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0.3), MaxValueValidator(0.8)]
    )
    difficulty_level=(
        (1,'difficult'),
        (2,'simple')
    )
    objective_level=(
        (1,'remining'),
        (2,'understanding'),
        (3,'creative'),
    )
    difficulty=models.IntegerField(
        choices=difficulty_level,
        default=1
    )
    # 1 ----> simple
    # 2 -----> difficult
    objective=models.IntegerField(
        choices=objective_level,
        default=1
    )

    def get_objective_level(self):
        return self.objective_level[self.objective][1]


    def get_difficulty_level(self):
        return self.difficulty_level[self.difficulty][1]


    def get_chapter_num(self):
        return self.subject.chapter_num
    # 1 ---> ramining
    # 2 ---> udestanding
    # 3 ----> creativety

    chapter_num=models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4)
        ]
    )



    def clean(self):
        if self.value < 0:
            raise ValidationError(_('Only numbers equal to 1 or greater are accepted.'))

    def __str__(self):
        return self.text



class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    text = models.CharField('Answer',max_length=255)
    is_correct =models.BooleanField('Correct answer',default=False)

    def __str__(self):
        return self.text



class Exam(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='exams')
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='exams')
    score = models.FloatField()
    data= models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return (""+self.subject.name+" exam To Student : "+self.student.user.username)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='exam_answers')
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='+')



class Event(models.Model):
    title = models.CharField(max_length=200)
    data = models.DateTimeField(default=now())
    position =models.CharField(max_length=200)

