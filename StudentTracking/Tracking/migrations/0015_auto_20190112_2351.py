# Generated by Django 2.1.4 on 2019-01-12 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tracking', '0014_auto_20190112_1853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherreport',
            name='activityID',
        ),
        migrations.RemoveField(
            model_name='teacherreport',
            name='studentID',
        ),
        migrations.AddField(
            model_name='teacherreport',
            name='asgactID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Tracking.AssActToStudent', verbose_name='asg act to stu'),
        ),
    ]
