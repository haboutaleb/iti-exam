from django.urls import path , include
from classroom.views import accounting,student,instructor
urlpatterns = [
    path('',accounting.home , name='home'),
    path('student/', include(([
                                   path('', student.SubjectListView.as_view(), name='exam_list'),
                                   path('exam/<int:subject_pk>', student.take_Exam, name='take_exam'),
                                   path('taken/', student.TakenExamListView.as_view(), name='taken_exam_list'),
                                   # path('quiz/<int:pk>/', student.take_quiz, name='take_quiz'),
                               ], 'classroom'), namespace='student')),

    path('instructor/', include(([
                                   path('', instructor.SubjectQustionsView.as_view(), name='subject_exam_list'),
                                   path('addqustion',instructor.Question_add ,name='qustion_add'),
                                   path('addQuestionAnswers/<int:question_pk>',instructor.Question_Answers_add , name='question_answers_add'),
                                   path('editQuestionAnswers/<int:question_pk>',instructor.Question_Answers_edit , name='question_answers_edit'),
                                   path('deleteQuestionAnswers/<int:question_pk>',instructor.Question_Answers_delete , name='question_answers_delete'),
                                    path('setdegree', instructor.set_subject_Exam_degree, name='Exam_degree'),
                                    path('taken',instructor.TakenExamListView.as_view() , name='taken_exam_list'),
                                    path('students',instructor.showStudents,name='students_show'),
                                    path('students/<int:student_pk>',instructor.showStudentExams,name='student_Exam_show'),
                               ], 'classroom'), namespace='instructor')),
]