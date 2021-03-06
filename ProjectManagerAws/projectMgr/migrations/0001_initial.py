# Generated by Django 3.1 on 2020-08-26 06:14

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profilePicture', models.CharField(max_length=200, null=True)),
                ('fullName', models.CharField(max_length=100, null=True)),
                ('bio', models.CharField(max_length=500, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdOn', models.DateTimeField(auto_now=True)),
                ('modifiedOn', models.DateTimeField()),
                ('textField', models.TextField()),
                ('deleted', models.BooleanField(default=False)),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('replyLink', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projectMgr.comment')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('isArchived', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('deadLine', models.DateTimeField(null=True)),
                ('comment', models.ManyToManyField(to='projectMgr.Comment')),
                ('createdBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projectIcreated', to=settings.AUTH_USER_MODEL)),
                ('people', models.ManyToManyField(related_name='project_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('stage', models.CharField(max_length=100)),
                ('priority', models.CharField(default='Normal', max_length=100)),
                ('deadLine', models.DateTimeField(null=True)),
                ('comment', models.ManyToManyField(to='projectMgr.Comment')),
                ('people', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('reporter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Ireported', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('DeadLine', models.DateTimeField(null=True)),
                ('comment', models.ManyToManyField(to='projectMgr.Comment')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taskgroupIcreated', to=settings.AUTH_USER_MODEL)),
                ('people', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taskgroup_set', to='projectMgr.project')),
            ],
        ),
        migrations.CreateModel(
            name='taskFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('filePath', models.CharField(max_length=200)),
                ('uploadedOn', models.DateTimeField(auto_now=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectMgr.task')),
                ('uploadedBy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='taskGroup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projectMgr.taskgroup'),
        ),
    ]
