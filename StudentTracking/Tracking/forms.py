from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from .models import Student, AssActToStudent, TeacherReport, AssActToTeacher, Homework

from .models import Teacher


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:  # keep configurations one place
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DateInput(forms.DateInput):
    input_type = 'date'


class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['studentName', 'studentSurname', 'studentDateOfBirth', 'schoolID', 'parentID', 'bookID']
        widgets = {
            'studentDateOfBirth': DateInput()
        }


class TeacherReportCreateForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(TeacherReportCreateForm, self).__init__(*args, **kwargs)
        self.user = user
        print(user)
        teacher = Teacher.objects.get(user_id=user)
        activities = AssActToTeacher.objects.filter(userID=teacher)
        queryset = AssActToStudent.objects.none()
        for act in activities:
            if AssActToStudent.objects.filter(activityID=act.activityID).exists():
                print(AssActToStudent.objects.filter(activityID=act.activityID))
                queryset |= AssActToStudent.objects.filter(activityID=act.activityID)

        self.fields['asgactID'].queryset = queryset

    class Meta:
        model = TeacherReport
        fields = ['asgactID', 'grade', 'stage', 'content', 'reportID', 'examResultID']


class HomeworkCreateForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(HomeworkCreateForm, self).__init__(*args, **kwargs)
        self.user = user
        print(user)
        teacher = Teacher.objects.get(user_id=user)
        activities = AssActToTeacher.objects.filter(userID=teacher)
        queryset = Homework.objects.none()
        for act in activities:

            if AssActToStudent.objects.filter(activityID=act.activityID).exists():
                print(AssActToStudent.objects.filter(activityID=act.activityID))
                queryset |= AssActToStudent.objects.filter(activityID=act.activityID)

        self.fields['assActToStuID'].queryset = queryset

    class Meta:
        model = Homework
        fields = ['homeworkName', 'givenDate', 'dueDate', 'assActToStuID']
