from MySQLdb import connections

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import connection
from django.shortcuts import render, redirect
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,)
from extra_views import InlineFormSet
from Tracking.forms import UserRegisterForm, StudentCreateForm, TeacherReportCreateForm, HomeworkCreateForm
from .models import (Activities, Student, AssActToStudent, TeacherReport, Teacher, Homework, ClassHours, AssActToTeacher)
from django.db.models import Count, Sum, Avg, Max


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)  #auto hash password
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login') #login page
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    current_user = request.user
    print(current_user)
    context = {
        'activities': Activities.objects.all(),
        'asgacts': AssActToStudent.objects.all(),
        'students': Student.objects.all(),
        'current_user': current_user,

    }

    studentDict = {}

    for student in Student.objects.all():
        for asgact in AssActToStudent.objects.filter(studentID=student.pk):
            if student.pk == asgact.studentID.pk:
                if not student.pk in studentDict:
                    studentDict[student.pk] = []
                    studentDict[student.pk].append(asgact.activityID)
                else:
                    studentDict[student.pk].append(asgact.activityID)
        context['studentDict'] = studentDict

    reports = TeacherReport.objects.filter(userID__user=request.user.id)

    context2 = {
        'reports': reports,
        'current_user': current_user,
        'homeworks': Homework.objects.all(),
        'classhours': ClassHours.objects.all(),
    }

    if current_user.is_superuser:
        return render(request, 'Tracking/home.html', context)
    else:
        return render(request, 'Tracking/home2.html', context2)


def statisticsActivity(request):

    activitycount = Activities.objects.all().values('activityName').annotate(total=Count('activityName'))
    studentcount = AssActToStudent.objects.all().values('studentID').annotate(total=Count('studentID'))
    total_paid = Activities.objects.all().aggregate(Sum('price'))
    avgprice = Activities.objects.aggregate(Avg('price'))
    maxprice = Activities.objects.aggregate(Max('price'))

    context = {


        'total_paid': total_paid,
        'activitycounts': activitycount,
        'avgprices': avgprice,
        'maxprices': maxprice,
        'studentcounts': studentcount,
    }

    return render(request, 'Tracking/statisticsActivity.html', context)


def statisticsStudent(request):
    activitycount = AssActToStudent.objects.all().values('activityID__activityName').annotate(total=Count('activityID__activityName'))

    cursor = connection.cursor()
    try:
        cursor.callproc('StudentCountbyID')
        studentcounts = cursor.fetchall()

    finally:
        cursor.close()

    stcnt = studentcounts
    context = {

        'activitycounts': activitycount,
        'studentcounts': stcnt,
    }

    return render(request, 'Tracking/statisticsStudent.html', context)


class ActivitiesListView(ListView):
    model = Activities
    context_object_name = 'activities'
    template_name = 'Tracking/home.html'


class TeacherReportListView(ListView):
    model = TeacherReport
    context_object_name = 'reports'
    template_name = 'Tracking/home2.html'


class TeacherReportCreateView(LoginRequiredMixin, CreateView, InlineFormSet):
    model = TeacherReport
    form_class = TeacherReportCreateForm

    def dispatch(self, *args, **kwargs):
        return super(TeacherReportCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(TeacherReportCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form): # bu method author_id kısmı null olamaz.
        obj = form.save(commit=False)
        obj.userID = Teacher.objects.get(user_id=self.request.user)
        obj.save()
        return super().form_valid(form)


class TeacherReportDetailView(DetailView):
    model = TeacherReport


class TeacherReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TeacherReport

    fields = ['asgactID', 'grade', 'stage', 'content', 'reportID', 'examResultID']

    def form_valid(self, form):  # bu method author_id kısmı null olamaz.
        obj = form.save(commit=False)
        obj.userID = Teacher.objects.get(user_id=self.request.user)
        obj.save()
        return super().form_valid(form)

    def test_func(self):
        if self.request.user:  #current logged in user equal to admin
            return True
        return False


class TeacherReportDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TeacherReport
    success_url = '/'

    def test_func(self):

        if self.request.user:  #current logged in user equal admin
            return True
        return False


class ActivitiesCreateView(LoginRequiredMixin, CreateView, InlineFormSet):
    model = Activities
    fields = ['activityName', 'activityTime', 'activityType', 'classifyAge', 'classifyStage', 'price']

    def form_valid(self, form):
        form.instance.author = self.request.user #current logged in user
        return super().form_valid(form)


class ActivitiesDetailView(DetailView):
    model = Activities


class ActivitiesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Activities
    fields = ['activityName', 'activityTime', 'activityType', 'classifyAge', 'classifyStage', 'price']

    def form_valid(self, form):
        form.instance.author = self.request.user    #current logged in user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user:  #current logged in user
            return True
        return False


class ActivitiesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Activities
    success_url = '/'

    def test_func(self):
        if self.request.user:  #current logged in user equal admin
            return True
        return False


class HomeworkCreateView(LoginRequiredMixin, CreateView, InlineFormSet):
    model = Homework
    form_class = HomeworkCreateForm

    def dispatch(self, *args, **kwargs):
        return super(HomeworkCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(HomeworkCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class HomeworkDetailView(DetailView):
    model = Homework


class HomeworkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Homework
    fields = ['homeworkName', 'givenDate', 'dueDate', 'assActToStuID']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user:  #current logged in user
            return True
        return False


class HomeworkDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Homework
    success_url = '/'

    def test_func(self):
        if self.request.user:  #current logged in user
            return True
        return False


class ClassHoursCreateView(LoginRequiredMixin, CreateView, InlineFormSet):
    model = ClassHours
    fields = ['starTime', 'endTime', 'activityID', 'classID']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ClassHoursDetailView(DetailView):
    model = ClassHours


class ClassHoursUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClassHours
    fields = ['starTime', 'endTime', 'activityID', 'classID']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user:  #current logged in user
            return True
        return False


class ClassHoursDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ClassHours
    success_url = '/'

    def test_func(self):
        if self.request.user:  #current logged in user
            return True
        return False


class StudentCreateView(LoginRequiredMixin, CreateView, InlineFormSet):
    model = Student

    form_class = StudentCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user #current logged in user
        return super().form_valid(form)


class StudentDetailView(DetailView):
    model = Student

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        if AssActToStudent.objects.filter(studentID=self.kwargs['pk']).exists():
            names = ""
            activityNameSet = AssActToStudent.objects.filter(studentID=self.kwargs['pk'])
            for activity in activityNameSet:
                print("xxx", type(activity.activityID))
                names = names + activity.activityID.activityName + ", "
            activityNameString = names[:-2]
        else:
            activityNameString = 'There is no activity assigned.'
        context['activityNameString'] = activityNameString
        print(activityNameString)
        return context


class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Student
    form_class = StudentCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user #current logged in user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user:  #current logged in user equal to admin
            return True
        return False


class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Student
    success_url = '/'

    def test_func(self):

        if self.request.user:  #current logged in user equal admin
            return True
        return False


class AsgActCreateView(LoginRequiredMixin, CreateView):

    model = AssActToStudent
    inlines = [StudentCreateView]
    fields = ['activityID', 'studentID']

    def form_valid(self, form):
        form.instance.user = self.request.user #current logged in user
        return super().form_valid(form)


class AsgActDetailView(DetailView):
    model = AssActToStudent


class AsgActUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AssActToStudent
    fields = ['activityID', 'studentID']

    def form_valid(self, form):
        form.instance.user = self.request.user #current logged in user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user:  #current logged in user equal to admin
            return True
        return False


class AsgActDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AssActToStudent
    success_url = '/'

    def test_func(self):
        if self.request.user:  #current logged in user equal admin
            return True
        return False


class AsgActTeacherCreateView(LoginRequiredMixin, CreateView):
    model = AssActToTeacher
    inlines = [StudentCreateView]
    fields = ['userID', 'activityID']

    def form_valid(self, form):  # bu method kısmı null olamaz.
        form.instance.user = self.request.user  # current logged in user
        return super().form_valid(form)


class AsgActTeacherDetailView(DetailView):
    model = AssActToTeacher


class AsgActTeacherUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AssActToTeacher
    fields = ['userID', 'activityID']

    def form_valid(self, form):  # bu method author_id kısmı null olamaz.
        form.instance.user = self.request.user  # current logged in user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user:  # current logged in user equal to admin
            return True
        return False


class AsgActTeacherDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AssActToTeacher
    success_url = '/'

    def test_func(self):
        if self.request.user:  # current logged in user equal admin
            return True
        return False
