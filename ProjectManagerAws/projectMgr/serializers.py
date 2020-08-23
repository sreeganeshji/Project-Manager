from .models import User, Project, TaskGroup, Task
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url','username','email']

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['url','name','description','people','isArchived','comment','created','createdBy','deadLine']

class TaskGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskGroup
        fields = ['url','name','description']

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['url','name','description','taskGroup']