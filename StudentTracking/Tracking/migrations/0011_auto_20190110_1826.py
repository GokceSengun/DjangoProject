# Generated by Django 2.1.4 on 2019-01-10 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tracking', '0010_teacherreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresult',
            name='studentID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tracking.Student', verbose_name='student'),
        ),
        migrations.AlterField(
            model_name='teacherreport',
            name='examResultID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tracking.ExamResult', verbose_name='exam Result'),
        ),
        migrations.AlterField(
            model_name='teacherreport',
            name='reportID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tracking.Reports', verbose_name='Report'),
        ),
        migrations.AlterField(
            model_name='teacherreport',
            name='userID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tracking.Teacher', verbose_name='Teacher name'),
        ),
    ]