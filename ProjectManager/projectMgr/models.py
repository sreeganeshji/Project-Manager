from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

'''
1. there are multiple users.
2. people can create a project. this can be treated as a large project involving many people as part of the team.
3. the project has multiple task groups. 
4. each task group has multpile tasks at different stages.
5. each tasks have multiple people associated with it belonging to the project.

the projects can be archived for later access after use.
'''


# Create your models here.
class User(AbstractUser):
    profilePicture = models.CharField(max_length=200,null=True)
    fullName = models.CharField(max_length=100,null=True)
    bio = models.CharField(null=True,max_length=500)
    pass


class Comment(models.Model):
    '''
    created by
    created on
    modified on
    linkedto(if none, first comment, else, reply)

    '''
    createdOn = models.DateTimeField(auto_now=True)
    modifiedOn = models.DateTimeField()
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    textField = models.TextField()
    replyLink = models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    deleted = models.BooleanField(default=False)

class Project(models.Model):
    '''
    need to have people associated with the project.
    one project can have many people and one person can be part of many projects. hence it could be a many to many relationship.

    the projects can have the option to be associated with teams. the team can be independant of the projects.
    everyone has the same permissions when it comes to creating the project. they cannot delete it for others.

    the project can have different tasks with different stages. i can have a one-one relationship to the datastructure which handles the event transitions.


    '''
    name = models.CharField(max_length=100)
    people = models.ManyToManyField(User,related_name="project_set")
    description = models.TextField()
    isArchived = models.BooleanField(default=False)
    comment = models.ManyToManyField(Comment)
    created = models.DateTimeField(auto_now=True)
    createdBy = models.ForeignKey(User,on_delete=models.CASCADE,related_name="projectIcreated",null=True)
    deadLine = models.DateTimeField(null=True)
    pass

class TaskGroup(models.Model):

    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='taskgroupIcreated',null=True)
    description = models.TextField()
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="taskgroup_set",null=True)
    comment = models.ManyToManyField(Comment)
    people = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now=True)
    DeadLine = models.DateTimeField(null=True)

class Task(models.Model):

    name = models.CharField(max_length=100)
    people = models.ManyToManyField(User)
    reporter = models.ForeignKey(User,related_name='Ireported',null=True,on_delete=models.PROTECT)
    description = models.TextField()
    taskGroup = models.ForeignKey(TaskGroup,on_delete=models.CASCADE,null=True)
    comment = models.ManyToManyField(Comment)
    created = models.DateTimeField(auto_now=True)
    stage = models.CharField(max_length=100) #initiate->in progress->review->done
    priority = models.CharField(max_length=100,default="Normal")
    deadLine = models.DateTimeField(null=True)
    pass

class taskFile(models.Model):
    name = models.CharField(max_length=100)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    filePath = models.CharField(max_length=200)
    uploadedBy = models.ForeignKey(User,on_delete=models.PROTECT)
    uploadedOn = models.DateTimeField(auto_now=True)


