from django.contrib import admin
from .models import (Teacher,
                     School,
                     Admins,
                     Addresses,
                     Parent,
                     Classes,
                     Activities,
                     Reports,
                     Books,
                     Payment,
                     StudentAddress,
                     Student,
                     AssActToStudent,
                     AssActToTeacher,
                     ClassHours,
                     Homework,
                     Exam,
                     ExamResult,
                     TeacherReport)
# Register your models here.


admin.site.register(Teacher)
admin.site.register(School)
admin.site.register(Admins)
admin.site.register(Addresses)
admin.site.register(Parent)
admin.site.register(Classes)
admin.site.register(Activities)
admin.site.register(Reports)
admin.site.register(Books)
admin.site.register(StudentAddress)
admin.site.register(Student)
admin.site.register(AssActToStudent)
admin.site.register(Payment)
admin.site.register(AssActToTeacher)
admin.site.register(ClassHours)
admin.site.register(Homework)
admin.site.register(Exam)
admin.site.register(TeacherReport)
admin.site.register(ExamResult)
