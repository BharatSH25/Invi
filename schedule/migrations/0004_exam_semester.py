# Generated by Django 4.2.1 on 2023-06-30 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_remove_exam_dept_remove_exam_exam_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='semester',
            field=models.CharField(choices=[('1-1', '1-1'), ('1-2', '1-2'), ('2-1', '2-1'), ('2-2', '2-2'), ('2-1', '2-1'), ('2-2', '2-2'), ('3-1', '3-1'), ('4-2', '4-2')], default='3-1', max_length=10),
        ),
    ]