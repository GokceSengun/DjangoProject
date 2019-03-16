from django.urls import path
from . import views
from .views import (
    ActivitiesDetailView,
    ActivitiesCreateView,
    ActivitiesUpdateView,
    ActivitiesDeleteView,
    AsgActCreateView,
    AsgActDetailView,
    AsgActUpdateView,
    AsgActDeleteView,
    TeacherReportCreateView,
    TeacherReportDetailView,
    TeacherReportUpdateView,
    TeacherReportDeleteView,
    StudentCreateView,
    StudentUpdateView,
    StudentDetailView,
    StudentDeleteView,
    HomeworkDeleteView,
    HomeworkCreateView,
    HomeworkDetailView,
    HomeworkUpdateView,
    ClassHoursCreateView,
    ClassHoursDeleteView,
    ClassHoursDetailView,
    ClassHoursUpdateView,
    AsgActTeacherCreateView,
    AsgActTeacherDeleteView,
    AsgActTeacherDetailView,
    AsgActTeacherUpdateView)


urlpatterns = [

    path('', views.home, name='tracking-home'),
    path('activities/<int:pk>/', ActivitiesDetailView.as_view(), name="activity-detail"), #localhost/post/1 falan yazınca id si 1 olan postun sayfası açılır.
    path('activities/new/', ActivitiesCreateView.as_view(), name="activity-create"),   #localhost/post/new  yeni post ekleme sayfası
    path('activities/<int:pk>/update/', ActivitiesUpdateView.as_view(), name="activity-update"), #localhost/post/1/update id si 1 olan postu update etme sayfası açılır.
    path('activities/<int:pk>/delete/', ActivitiesDeleteView.as_view(), name="activity-delete"),
    path('assignactivity/new/', AsgActCreateView.as_view(), name="assign-activity"),
    path('assignactivity/<int:pk>/update/', AsgActUpdateView.as_view(), name="assign-activity-update"),
    path('assignactivity/<int:pk>/', AsgActDetailView.as_view(), name="assign-activity-detail"),
    path('assignactivity/<int:pk>/delete/', AsgActDeleteView.as_view(), name="assign-activity-delete"),
    path('assignactivityteacher/new/', AsgActTeacherCreateView.as_view(), name="assign-activity-teacher"),
    path('assignactivityteacher/<int:pk>/update/', AsgActTeacherUpdateView.as_view(), name="assign-activity-teacher-update"),
    path('assignactivityteacher/<int:pk>/', AsgActTeacherDetailView.as_view(), name="assign-activity-teacher-detail"),
    path('assignactivityteacher/<int:pk>/delete/', AsgActTeacherDeleteView.as_view(), name="assign-activity-teacher-delete"),
    path('teacherreport/new/', TeacherReportCreateView.as_view(), name="report-create"),
    path('teacherreport/<int:pk>/', TeacherReportDetailView.as_view(), name="teacher-report-detail"),
    path('teacherreport/<int:pk>/update/', TeacherReportUpdateView.as_view(), name="teacher-report-update"),
    path('teacherreport/<int:pk>/delete/', TeacherReportDeleteView.as_view(), name="teacher-report-delete"),
    path('student/<int:pk>/', StudentDetailView.as_view(), name="student-detail"),
    path('student/new/', StudentCreateView.as_view(), name="student-create"),
    path('student/<int:pk>/update/', StudentUpdateView.as_view(), name="student-update"),
    path('student/<int:pk>/delete/', StudentDeleteView.as_view(), name="student-delete"),
    path('homework/<int:pk>/', HomeworkDetailView.as_view(), name="homework-detail"),
    path('homework/new/', HomeworkCreateView.as_view(), name="homework-create"),
    path('homework/<int:pk>/update/', HomeworkUpdateView.as_view(), name="homework-update"),
    path('homework/<int:pk>/delete/', HomeworkDeleteView.as_view(), name="homework-delete"),
    path('classhours/<int:pk>/', ClassHoursDetailView.as_view(), name="classhours-detail"),
    path('classhours/new/', ClassHoursCreateView.as_view(), name="classhours-create"),
    path('classhours/<int:pk>/update/', ClassHoursUpdateView.as_view(), name="classhours-update"),
    path('classhours/<int:pk>/delete/', ClassHoursDeleteView.as_view(), name="classhours-delete"),
    path('statistics/activity/', views.statisticsActivity, name="statistics-activity"),
    path('statistics/student/', views.statisticsStudent, name="statistics-student"),

]