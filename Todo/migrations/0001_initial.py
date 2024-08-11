# Generated by Django 5.1 on 2024-08-09 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('due_date', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('todo', 'Todo'), ('in progress', 'In progress'), ('done', 'Done')], max_length=50, null=True)),
            ],
        ),
    ]
