import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),

                ('due_date', models.DateField(default=datetime.datetime(2023, 12, 20, 19, 30, 35, 207411))),

                ('due_date', models.DateField(default=datetime.datetime(2023, 12, 20, 14, 57, 34, 456188))),

                ('status', models.CharField(choices=[('P', 'In Process'), ('H', 'On Hold'), ('C', 'Completed')], default='P', max_length=1)),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),

                ('due_date', models.DateField(default=datetime.datetime(2023, 12, 20, 19, 30, 35, 207585))),

                ('due_date', models.DateField(default=datetime.datetime(2023, 12, 20, 14, 57, 34, 457892))),

                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('P', 'In Process'), ('H', 'On Hold'), ('C', 'Completed')], default='P', max_length=1)),
                ('priority', models.CharField(choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')], default='H', max_length=6)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_tasks', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.project')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('Qua', 'Quality/Testing'), ('Dev', 'Developers'), ('Des', 'Design'), ('Arq', 'Arquitect'), ('Man', 'Manager')], default='Qua', max_length=3)),
                ('image_url', models.CharField(default='/static/profile-image.jpeg', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.project')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
