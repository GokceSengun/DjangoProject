# Generated by Django 2.1.4 on 2019-01-09 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tracking', '0003_auto_20190110_0046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentType', models.CharField(choices=[('cash', 'CASH'), ('creditcard', 'CREDITCARD')], default='CASH', max_length=20)),
                ('assActToStuID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tracking.AssActToStudent', verbose_name='assigned activity')),
            ],
        ),
    ]