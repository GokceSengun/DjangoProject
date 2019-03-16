from django.db import models
from django.contrib.auth.models import User, PermissionsMixin


from django.urls import reverse


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


class Teacher(Users):

    email = models.CharField(max_length=50, verbose_name='email')

    def __str__(self):
        return f'{self.user.username}'


class Admins(Users):

    email = models.CharField(max_length=50, verbose_name='email')

    def __str__(self):
        return f'{self.user.username}'


class School(models.Model):
    schoolName = models.CharField(max_length=100, verbose_name='schoolname')
    location = models.CharField(max_length=250)

    def __str__(self):
        return self.schoolName


class Parent(models.Model):
    parentName = models.CharField(max_length=100, verbose_name='parentName')
    parentSurname = models.CharField(max_length=250)
    parentDateOfBirth = models.DateField()

    def __str__(self):
        return self.parentName


class Addresses(models.Model):
    country = models.CharField(max_length=50, verbose_name='country')
    city = models.CharField(max_length=50)
    openAddress = models.TextField()

    def __str__(self):
        return self.openAddress


class Books(models.Model):

    genre = models.CharField(max_length=50, verbose_name='genre')
    title = models.CharField(max_length=50, verbose_name='title')
    content = models.TextField(verbose_name='content')

    def __str__(self):
        return self.title


class Classes(models.Model):

    className = models.CharField(max_length=50, verbose_name='class name')

    def __str__(self):
        return self.className


class Activities(models.Model):
    activityName = models.CharField(max_length=50, verbose_name='activity name')
    activityTime = models.CharField(max_length=50, verbose_name='activity time')
    activityType = models.CharField(max_length=50, verbose_name='activity type')
    classifyAge = models.CharField(max_length=50, verbose_name='Age', blank=True, null=True)
    classifyStage = models.CharField(max_length=50, verbose_name='Stage', blank=True, null=True)
    price = models.IntegerField(verbose_name='price')

    def __str__(self):
        return self.activityName

    def get_absolute_url(self):
        return reverse('activity-detail', kwargs={'pk': self.pk})


class Reports(models.Model):
    reportName = models.CharField(max_length=50, verbose_name='report name')
    reportType = models.CharField(max_length=50, verbose_name='report type')
    reportContent = models.TextField(verbose_name='content')

    def __str__(self):
        return self.reportName


class Student(models.Model):
    studentName = models.CharField(max_length=50, verbose_name='student name')
    studentSurname = models.CharField(max_length=50, verbose_name='student surname')
    studentDateOfBirth = models.DateField(max_length=50, verbose_name='student Date birth')
    schoolID = models.ForeignKey(School, verbose_name='School ', null=True, blank=True, on_delete=models.SET_NULL)
    parentID = models.ForeignKey(Parent, verbose_name='Parent', on_delete=models.CASCADE)
    bookID = models.ForeignKey(Books, verbose_name='Book ', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.studentName

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk': self.pk})


class StudentAddress(models.Model):
    studentID = models.ForeignKey(Student, verbose_name='student ID', on_delete=models.CASCADE)
    addressID = models.ForeignKey(Addresses, verbose_name='Address ID', on_delete=models.CASCADE)

    def __str__(self):
        return self.addressID.openAddress


class AssActToStudent(models.Model):
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='student id')
    activityID = models.ForeignKey(Activities, on_delete=models.CASCADE, verbose_name='activity id')

    def __str__(self):
        return f'{self.studentID}\'s activity is '+f'{self.activityID}'

    def get_absolute_url(self):
        return reverse('assign-activity-detail', kwargs={'pk': self.pk})


class Payment(models.Model):
    payment_CHOICES = (
        ('cash', 'CASH'),
        ('creditcard', 'CREDITCARD'),
    )

    paymentType = models.CharField(max_length=20, choices=payment_CHOICES, default='CASH')
    assActToStuID = models.ForeignKey(AssActToStudent, verbose_name='assigned activity', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.assActToStuID}.The activity price is ' + f'{self.assActToStuID.activityID.price}'


class AssActToTeacher(models.Model):
    userID = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='teacher name')
    activityID = models.ForeignKey(Activities, on_delete=models.CASCADE, verbose_name='activity id')

    def __str__(self):
        return f'{self.activityID}\'s teacher is '+f'{self.userID}'

    def get_absolute_url(self):
        return reverse('assign-activity-teacher-detail', kwargs={'pk': self.pk})


class ClassHours(models.Model):
    starTime = models.TimeField(verbose_name='start time')
    endTime = models.TimeField(verbose_name='end time')
    activityID = models.OneToOneField(Activities, on_delete=models.CASCADE, verbose_name='activity id')
    classID = models.ForeignKey(Classes, on_delete=models.CASCADE, verbose_name='class id')

    def __str__(self):
        return f'{self.classID}'

    def get_absolute_url(self):
        return reverse('classhours-detail', kwargs={'pk': self.pk})


class Homework(models.Model):

    homeworkName = models.CharField(max_length=100, verbose_name='homework name')
    givenDate = models.DateField(verbose_name='given date')
    dueDate = models.DateTimeField(verbose_name='due date')
    assActToStuID = models.OneToOneField(AssActToStudent, verbose_name='assigned activity id', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.assActToStuID}.The homework for given student is ' + f'{self.homeworkName}'

    def get_absolute_url(self):
        return reverse('homework-detail', kwargs={'pk': self.pk})


class Exam(models.Model):
    subject = models.CharField(max_length=100, verbose_name='subject')
    Date = models.DateTimeField(verbose_name='Exam Date Time')
    activityID = models.ForeignKey(Activities, on_delete=models.CASCADE, verbose_name='activity id')

    def __str__(self):
        return f'{self.activityID}\'s exam'


class ExamResult(models.Model):
    result = models.IntegerField(verbose_name='result')
    examID = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='exam ID')
    studentID = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, verbose_name='student')

    def __str__(self):
        return str(self.result)


class TeacherReport(models.Model):
    grade = models.CharField(max_length=50, verbose_name='grade')
    stage = models.CharField(max_length=50, verbose_name='stage')
    content = models.TextField(verbose_name='content')
    reportID = models.ForeignKey(Reports, on_delete=models.CASCADE, verbose_name='Report')
    userID = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name='Teacher name')
    examResultID = models.ForeignKey(ExamResult, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='exam Result')
    asgactID = models.ForeignKey(AssActToStudent, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='asg act to stu')

    def __str__(self):
        return self.reportID.reportName

    def get_absolute_url(self):
        return reverse('teacher-report-detail', kwargs={'pk': self.pk})

