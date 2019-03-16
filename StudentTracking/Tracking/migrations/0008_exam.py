# Generated by Django 2.1.4 on 2019-01-09 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tracking', '0007_homework'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='subject')),
                ('Date', models.DateTimeField(verbose_name='Exam Date Time')),
                ('activityID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tracking.Activities', verbose_name='activity id')),
            ],
        ),
    ]