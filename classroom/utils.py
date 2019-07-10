from classroom.models import Question ,Subject
import random



class Exam:
    def __init__(self,questions:list,examFitness:dict):
        self.examFitnes=examFitness
        self.questions=questions



class GeneticExam:
    def __init__(self,subject_pk):
        self.subject_pk=subject_pk
        self.subject=Subject.objects.get(pk=subject_pk)
        self.AllQuestion = Question.objects.filter(subject=subject_pk)
        self.selected = []
        self.exam_Question_num = 15
        for ele in self.AllQuestion:
            self.selected.append((ele.id, ele.value,ele.difficulty,ele.objective,ele.chapter_num),)


    def initPopulate(self,questionArr:list):
        if len(questionArr) < 7*self.exam_Question_num:
            return None
        tempAllQuestions=questionArr.copy()
        examSimplesNum =len(tempAllQuestions)//self.exam_Question_num
        examArr=[]
        for _ in range(examSimplesNum):
            tempExamArr=[]
            for _ in range(self.exam_Question_num):
                tempOneQuestion=random.choice(tempAllQuestions)
                tempExamArr.append(tempOneQuestion)
                tempAllQuestions.remove(tempOneQuestion)
            fitness= self.get_fitness(tempExamArr)
            exam_object=Exam(tempExamArr,fitness)
            examArr.append(exam_object)
        return examArr


    def crossOver(self,exams:list ):
        exam_len=len(exams)
        crossover_Exams=[]
        if len(exams)%2 == 0:
            num=exam_len//2
        else:
            num=(exam_len//2) +1
        flag = 0
        for _ in range(num):
            parent_1=exams[flag%exam_len].questions
            parent_2=exams[(flag+1)%exam_len].questions
            crossover_index = random.randrange(1, len(parent_1))
            child_1 = parent_1[:crossover_index] + parent_2[crossover_index:]
            child_2 = parent_2[:crossover_index] + parent_1[crossover_index:]
            crossover_Exams.append(child_1)
            crossover_Exams.append(child_2)
            flag+=2
            crossover_Exams_with_fitness=[]
        for ele in crossover_Exams:
            fitness= self.get_fitness(ele)
            exam_object=Exam(ele,fitness)
            crossover_Exams_with_fitness.append(exam_object)
        return crossover_Exams_with_fitness





    def get_fitness(self,tempExamArr):
        exam_difficult=0
        exam_understanding=0
        exam_remining=0
        chapter_qustion = []
        for _ in range(self.subject.chapter_num):
            chapter_qustion.append(0)

        for ele in tempExamArr:
            if ele[2] == 1:
                exam_difficult+= 1

            if ele[3] == 1:
                exam_remining += 1
            elif ele[3] == 2 :
                exam_understanding+= 1

            chapter_qustion[(ele[4])-1] +=1
        return {
            'difficult_num' : exam_difficult,
            'understanding_num':exam_understanding,
            'ramining_num':exam_remining,
            'qustion_chapter' : chapter_qustion
        }












    def population(self,examArr:list):
        like_demand=None
        if not examArr:
            return None
        for i in range(7):
            print("---------------------- GEN",i+1,"---------------------")
            for ele in examArr:
                print(ele.questions)
                if ele.examFitnes['difficult_num'] == self.subject.question_num_difficult \
                    and ele.examFitnes['understanding_num'] == self.subject.question_num_understanding\
                    and ele.examFitnes['ramining_num'] == self.subject.question_num_ramining\
                    and not 0 in ele.examFitnes['qustion_chapter']\
                    and not 1 in ele.examFitnes['qustion_chapter']\
                    and not 2 in ele.examFitnes['qustion_chapter']:
                    return ele

                elif   ( abs(ele.examFitnes['difficult_num'] - self.subject.question_num_difficult) ==1 \
                    and ele.examFitnes['understanding_num'] == self.subject.question_num_understanding\
                    and ele.examFitnes['ramining_num'] == self.subject.question_num_ramining\
                    and not 0 in ele.examFitnes['qustion_chapter']\
                    and not 1 in ele.examFitnes['qustion_chapter']\
                    and not 2 in ele.examFitnes['qustion_chapter'])\
                            or \
                    (abs(ele.examFitnes['understanding_num'] - self.subject.question_num_understanding) == 1 \
                     and ele.examFitnes['difficult_num'] == self.subject.question_num_difficult \
                     and ele.examFitnes['ramining_num'] == self.subject.question_num_ramining \
                     and not 0 in ele.examFitnes['qustion_chapter'] \
                     and not 1 in ele.examFitnes['qustion_chapter']\
                     and not 2 in ele.examFitnes['qustion_chapter'])\
                        or \
                    (abs(ele.examFitnes['ramining_num'] - self.subject.question_num_ramining) == 1 \
                     and ele.examFitnes['difficult_num'] == self.subject.question_num_difficult \
                     and ele.examFitnes['understanding_num'] == self.subject.question_num_understanding \
                     and not 0 in ele.examFitnes['qustion_chapter']\
                     and not 1 in ele.examFitnes['qustion_chapter']\
                     and not 2 in ele.examFitnes['qustion_chapter'])\
                        :
                    like_demand=ele
                    # muatete
            if like_demand:
                return like_demand
            examArr=self.crossOver(examArr)
        print("we need to do anther population")
        return self.population(self.initPopulate(self.selected))


    def get_Exam(self):
        return self.population(self.initPopulate(self.selected))