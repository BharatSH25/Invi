# Generated by Django 4.2.1 on 2023-06-30 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_exam_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='dept',
            field=models.CharField(choices=[('it', 'information technology'), ('eee', 'electrical'), ('cse', 'computer science'), ('ece', 'electronics and communication'), ('mca', 'master of computer application')], default='cse', max_length=3),
        ),
    ]
