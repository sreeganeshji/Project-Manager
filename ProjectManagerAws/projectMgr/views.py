from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from . import forms
from . import models
from datetime import datetime

#rest framework
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, TaskGroupSerializer, TaskSerializer, ProjectSerializer

# notification
from actstream import action
from actstream.models import actor_stream
from actstream.models import action_object_stream
from actstream.models import target_stream
from actstream.models import followers, following
from actstream.actions import follow, unfollow

from allauth.account.forms import LoginForm, SignupForm


# Create your views here.

def signin(request:HttpRequest):
    '''
    perform login using credentials email and pass
    '''
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            credentials = form.user_credentials()
            user = authenticate(request, username = credentials['username'], password = credentials['password'])
            print("user is ", user)
            if user:
                login(request,user)
                print('is authenticated', user.is_authenticated)
                print("login successful")
                return redirect('projectMgr:userhome')


        return render(request, 'projectMgr/signin.html', {'form': form})


    form = LoginForm()
    return render(request,'projectMgr/signin.html', {'form':form})


def homepage(request: HttpRequest):
    pass
    # defines the homepage
    '''
    needs to have links to signin and signup.
    have tab on about/contact
    have sidebar point to useful links.
    have body showing information about the product.

    '''
    print("at homepage")
    error = None
    if request.user.is_authenticated:
        return redirect('projectMgr:userhome')

    if request.method == "POST":
        form = forms.signIn(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                print('printing user', user)
                login(request, user)
                return redirect('projectMgr:userhome')
            error = "Please verify your credentials."


    else:
        form = forms.signIn()

    return render(request, 'projectMgr/homepage.html', {'form1': form, 'error': error})


def about(request:HttpRequest):
    return render(request,'projectMgr/about.html')


def signUp(request: HttpRequest):
    '''
    receive the login details and create a user.
    if all is successful, redirect to the logged in homepage

    :param request:
    :return:
    '''
    print("trying to signup")
    if request.user.is_authenticated:
        return redirect('projectMgr:userhome')

    if request.method == "POST":
        form = forms.signUp(request.POST)
        print("request.POST", request.POST)
        if form.is_valid():
            print("form is validated")

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            print(username, password, email)
            print("authenticate before model creation ", authenticate(request, username=username, password=password))
            user = models.User.objects.create_user(username, email, password)
            user.save()
            print("authenticate after model creation ",
                  authenticate(request, username=username, password=user.password))
            print(user)
            login(request, user)
            print("user logged in")
            return redirect('projectMgr:userhome')
    else:
        print("not POST")
        form = forms.signUp()

    return render(request, 'projectMgr/signup.html', {'form': form})
    pass


def userHome(request: HttpRequest):
    '''
    need to display user specific information related to the actual functionality of hte product.
    shwo the list of projects the user is associated with.
    list of teams the user is a part of.

    options ot create new teams and projects.

    need to hence create list and detail views of projects, teams, etc.
    need to have a way to search for the users based on thier username or email id.
    they should also be able to search for projects in this manner.
    when they are in the detail view of the team, they can have an option to search for projects nad members in thier own team.

    in their homepage, they can search for projects that they have been a part of.
    the body can list all the projects they are a part of. irrespective of who has created it.
    :param request:
    :return:
    choice1:can either just send the user and extract the different sets form it
    choice2: can pass multiple contexts.
    need to
    '''

    user = None
    print(request.user)
    if request.user.is_authenticated:
        user = request.user
    else:
        print("cannot authenticate")
        return redirect("projectMgr:homepage")


    listSet = []
    followingObjects = following(request.user)
    for object in following(request.user):
        listSet.append(target_stream(object)[:3])



    return render(request, 'projectMgr/userhome.html', {'thisUser': user,'list':list,'following':followingObjects,'listSet':listSet})


def logoutReq(request: HttpRequest):
    logout(request)
    return redirect("projectMgr:homepage")


def projectDetail(request: HttpRequest, projectid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')
    '''

    :param request:
    :return:
    '''
    thisProject = models.Project.objects.get(id=projectid)
    print(thisProject.name)
    commentForm = forms.createComment()
    commentSet = thisProject.comment.all()
    stream = target_stream(thisProject)

    return render(request, 'projectMgr/projectDetail.html',
                  {'project': thisProject, 'commentForm': commentForm, 'commentSet': commentSet,
                   'thisUser': request.user,'nocomm':len(commentSet),'stream':stream})

    pass

def followProject(request:HttpRequest, projectid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')
    thisProject = models.Project.objects.get(id=projectid)
    if thisProject in following(request.user, models.Project):
        unfollow(request.user, thisProject)
    else:
        follow(request.user, thisProject)


    return redirect('projectMgr:projectDetail',projectid=projectid)

def projectDetailEdit(request: HttpRequest, projectid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    thisProject = models.Project.objects.get(id=projectid)

    if request.method == "POST":
        form = forms.editProject(request.POST, nameVal=thisProject.name, descriptionVal=thisProject.description)

        print('form start', form, 'form end')
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            thisProject.name = name
            thisProject.description = description
            thisProject.save()
            # delete task activitiy
            action.send(request.user, verb="edited project", action_object=thisProject,
                        target=None)
            return redirect('projectMgr:projectDetail', projectid)
    else:
        form = forms.editProject(nameVal=thisProject.name, descriptionVal=thisProject.description)

    return render(request, 'projectMgr/projectDetailEdit.html',
                  {"form": form, "project": thisProject, "thisUser": request.user})


def taskDetailComment(request: HttpRequest, projectid, taskGroupId, taskid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    thisTask = models.Task.objects.get(id=taskid)
    if request.method == 'POST':
        commentForm = forms.createComment(request.POST)
        if commentForm.is_valid():
            text = commentForm.cleaned_data['Comment']
            newComment = models.Comment.objects.create(createdBy=request.user, textField=text,
                                                       modifiedOn=datetime.now())
            newComment.save()
            thisTask.comment.add(newComment)
            thisTask.save()
            # comment on task activitiy
            action.send(request.user, verb="commented on", action_object=thisTask,
                        target=models.TaskGroup.objects.get(id=taskGroupId))

    return redirect('projectMgr:taskDetail', projectid=projectid, taskGroupId=taskGroupId, taskid=taskid)

def followTaskGroup(request:HttpRequest, projectid, taskGroupId):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')
    thisProject = models.Project.objects.get(id=projectid)
    thisTaskGroup = models.TaskGroup.objects.get(id=taskGroupId)
    if thisTaskGroup in following(request.user, models.TaskGroup):
        unfollow(request.user, thisTaskGroup)
    else:
        follow(request.user, thisTaskGroup)
        # action.send(request.user,verb='started following', action_object=None, target=thisTaskGroup)
        # action.send(request.user, verb='started following', action_object=thisTaskGroup, target=thisProject)

    return redirect('projectMgr:taskGroupDetail',projectid=projectid, taskGroupId=taskGroupId)

def taskGroupDetailEdit(request: HttpRequest, projectid, taskGroupId):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    thisProject = models.Project.objects.get(id=projectid)
    thisTaskGroup = models.TaskGroup.objects.get(id=taskGroupId)

    if request.method == "POST":
        form = forms.editTaskGroup(request.POST, nameVal=thisTaskGroup.name, descriptionVal=thisTaskGroup.description, )

        # print('form start', form, 'form end')
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            thisTaskGroup.name = name
            thisTaskGroup.description = description
            thisTaskGroup.save()
            # edit taskgroup activitiy
            action.send(request.user, verb="edited taskgroup", action_object=thisTaskGroup,
                        target=models.Project.objects.get(id=projectid))
            return redirect('projectMgr:taskGroupDetail', projectid, taskGroupId)
    else:
        form = forms.editTaskGroup(nameVal=thisTaskGroup.name, descriptionVal=thisTaskGroup.description)

    return render(request, 'projectMgr/taskGroupDetailEdit.html',
                  {"form": form, "project": thisProject, "taskGroup": thisTaskGroup, "thisUser": request.user})


def taskGroupDetailComment(request: HttpRequest, projectid, taskGroupId):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    thisTaskGroup = models.TaskGroup.objects.get(id=taskGroupId)
    if request.method == 'POST':
        commentForm = forms.createComment(request.POST)
        if commentForm.is_valid():
            text = commentForm.cleaned_data['Comment']
            newComment = models.Comment.objects.create(createdBy=request.user, textField=text,
                                                       modifiedOn=datetime.now())
            newComment.save()
            thisTaskGroup.comment.add(newComment)
            thisTaskGroup.save()
            # comment on taskgroup activitiy
            action.send(request.user, verb="commented", target=thisTaskGroup)
            action.send(request.user, verb="commented in ", action_object=thisTaskGroup,
                        target=models.Project.objects.get(id=projectid))

    return redirect('projectMgr:taskGroupDetail', projectid=projectid, taskGroupId=taskGroupId)


def projectDetailComment(request: HttpRequest, projectid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    thisProject = models.Project.objects.get(id=projectid)
    if request.method == 'POST':
        commentForm = forms.createComment(request.POST)
        if commentForm.is_valid():
            text = commentForm.cleaned_data['Comment']
            newComment = models.Comment.objects.create(createdBy=request.user, textField=text,
                                                       modifiedOn=datetime.now())
            newComment.save()
            thisProject.comment.add(newComment)
            thisProject.save()
            # comment on project activitiy
            action.send(request.user, verb="commented ", action_object=None,
                        target=models.Project.objects.get(id=projectid))

    return redirect('projectMgr:projectDetail', projectid=projectid)


def taskDetail(request: HttpRequest, projectid, taskGroupId, taskid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    '''

    :param request:
    :return:
    '''
    thisProject = models.Project.objects.get(id=projectid)
    thisTaskGroup = models.TaskGroup.objects.get(id=taskGroupId)
    thisTask = models.Task.objects.get(id=taskid)
    thisUser = request.user

    commentForm = forms.createComment
    commentSet = thisTask.comment.all()
    stream = action_object_stream(thisTask)

    '''
    need multiple forms to fill in the details of the task.
    1.description
    2.attachment
    3.comment
    '''

    return render(request, 'projectMgr/taskDetail.html',
                  {'project': thisProject, 'taskGroup': thisTaskGroup, 'task': thisTask, 'commentForm': commentForm,
                   'commentSet': commentSet, 'thisUser': thisUser, 'stream':stream})

    pass

def followTask(request:HttpRequest, projectid, taskGroupId, taskid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')
    thisProject = models.Project.objects.get(id=projectid)
    thisTaskGroup = models.TaskGroup.objects.get(id = taskGroupId)
    thisTask = models.Task.objects.get(id=taskid)
    if thisTask in following(request.user, models.Task):
        unfollow(request.user, thisTask)
    else:
        follow(request.user, thisTask)
        # action.send(request.user, verb="started following", target=thisTask)
        # action.send(request.user, verb="started following", action_object=thisTask, target=thisProject)
        # action.send(request.user, verb="started following", action_object=thisTask, target=thisTaskGroup)

    return redirect('projectMgr:taskDetail',projectid=projectid, taskGroupId=taskGroupId, taskid=taskid)


def projectCreate(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    '''

    :param request:
    :return:
    '''
    # assuming user is authenticated

    print('request method is ', request.method)

    if request.method == 'POST':
        form = forms.createProject(request.POST)
        if form.is_valid():
            print("form is validated")
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            print("project", name, description)
            project = models.Project(name=name, description=description, isArchived=False,createdBy=request.user,created=datetime.now)
            project.save()
            project.people.add(request.user)
            project.save()
            print("project created")
            # create project activitiy
            action.send(request.user, verb="created project", action_object=project,
                        target=None)
            # request.session['current_projectid'] = project.id
            if "choose team" in request.POST:
                return redirect('projectMgr:chooseProjectMates', project.id)
            else:
                return redirect('projectMgr:projectDetail', projectid=project.id)
        else:
            print(request.POST, 'not valid')
    else:
        form = forms.createProject()

    return render(request, 'projectMgr/createProject.html', {'form': form, "thisUser": request.user})


def addToProject(request:HttpRequest,projectid,userid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')
    project = models.Project.objects.get(id=projectid)
    project.people.add(models.User.objects.get(id=userid))
    # add user activitiy
    action.send(request.user, verb="added user", action_object=models.User.objects.get(id=userid),
                target=models.Project.objects.get(id=projectid))
    return redirect('projectMgr:chooseProjectMates',projectid=projectid)


def chooseProjectMates2(request: HttpRequest, projectid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    '''

    :param request:
    :return:
    '''

    # projectid = request.session.get('current_projectid')
    # print("inputs",request,projectid)
    project = models.Project.objects.get(id=projectid)
    projectLabel = project.name
    print(request.method)

    results = models.User.objects.all().exclude(username__in=[person.username for person in project.people.all()])[:20]

    if request.method == "POST":

        form = forms.chooseMates2(request.POST)

        if form.is_valid():
            '''
            get the first 20 matches for the search query.
            '''

            search = form.cleaned_data.get('search')
            searchType = form.cleaned_data.get('searchType')
            print('search,searchtype', search, searchType)
            if searchType == 'email':
                results = models.User.objects.filter(email__contains=search)
            elif searchType == 'username':
                results = models.User.objects.filter(username__contains=search)

            results = results.exclude(username__in=[person.username for person in project.people.all()])[:20]


    else:
        form = forms.chooseMates2()

    return render(request, 'projectMgr/selectProjectMates.html',
                  context={'form': form, 'results': results, 'head': projectLabel,
                           'project': project, "thisUser": request.user})


def chooseProjectMates(request: HttpRequest, projectid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    '''

    :param request:
    :return:
    '''

    # projectid = request.session.get('current_projectid')
    # print("inputs",request,projectid)
    project = models.Project.objects.get(id=projectid)
    projectLabel = project.name
    print(request.method)

    results = models.User.objects.all().exclude(username__in=[person.username for person in project.people.all()])[:20]
    people = [[user.username, ((user.username + "\t-\t" + user.email) if user.email else user.username)] for user in
              results]

    if request.method == "POST":

        form = forms.chooseMates(request.POST, peopleChoice=people)

        if form.is_valid():
            '''
            get the first 20 matches for the search query.
            '''

            selectedPeople = form.cleaned_data.get('people')
            print("selected people", selectedPeople)
            if len(selectedPeople) > 0:
                # add people to project and move to project detail view.
                for peopleUserName in selectedPeople:
                    person = models.User.objects.get(username=peopleUserName)
                    project.people.add(person)
                project.save()

            search = form.cleaned_data.get('search')
            searchType = form.cleaned_data.get('searchType')
            print('search,searchtype', search, searchType)
            if searchType == 'email':
                results = models.User.objects.filter(email__contains=search)
            elif searchType == 'username':
                results = models.User.objects.filter(username__contains=search)

            results = results.exclude(username__in=[person.username for person in project.people.all()])[:20]
            people = [[user.username, ((user.username + "\t-\t" + user.email) if user.email else user.username)] for
                      user in results]
            form = forms.chooseMates(request.POST, peopleChoice=people)

            if "Done" in request.POST:
                return redirect('projectMgr:projectDetail', projectid)

    else:
        form = forms.chooseMates(peopleChoice=people)

    return render(request, 'projectMgr/selectProjectMates.html',
                  context={'form': form, 'results': results, 'head': projectLabel, 'error': form.errors,
                           'project': project, "thisUser": request.user})


def chooseTaskGroupMates(request: HttpRequest, projectid, taskGroupId):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    thisTaskGroup = models.TaskGroup.objects.get(id=taskGroupId)
    thisTaskProject = thisTaskGroup.project
    result = thisTaskProject.people.all().exclude(
        username__in=[person.username for person in thisTaskGroup.people.all()])[:20]

    peopleChoice = [
        [user.username, (user.username + '\t' + user.email)] if user.email else [user.username, (user.username)] for
        user in result]

    if request.method == 'POST':
        form = forms.chooseMates(request.POST, peopleChoice=peopleChoice)
        if form.is_valid():
            selectedPeople = form.cleaned_data.get('people')
            if len(selectedPeople) > 0:
                for personName in selectedPeople:
                    person = models.User.objects.get(username=personName)
                    thisTaskGroup.people.add(person)
                thisTaskGroup.save()

            if "Done" in request.POST:
                return redirect('projectMgr:taskGroupDetail', projectid=thisTaskProject.id,
                                taskGroupId=thisTaskGroup.id)

            search = form.cleaned_data['search']
            searchType = form.cleaned_data['searchType']
            if searchType == 'email':
                result = thisTaskProject.people.filter(email__contains=search).exclude(
                    username__in=[person.username for person in thisTaskGroup.people.all()])[:20]
            elif searchType == 'username':
                result = thisTaskProject.people.filter(username__contains=search).exclude(
                    username__in=[person.username for person in thisTaskGroup.people.all()])[:20]
            peopleChoice = [
                [user.username, (user.username + '\t' + user.email)] if user.email else [user.username, (user.username)]
                for user in result]
            form = forms.chooseMates(request.POST, peopleChoice=peopleChoice)

    else:
        form = forms.chooseMates(peopleChoice=peopleChoice)
    return render(request, 'projectMgr/selectTaskGroupMates.html',
                  {'form': form, 'project': models.Project.objects.get(id=projectid), 'task': thisTaskGroup, "thisUser": request.user})


def addToTaskGroup(request:HttpRequest,projectid,taskGroupId,userid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')
    taskgroup = models.TaskGroup.objects.get(id=taskGroupId)
    taskgroup.people.add(models.User.objects.get(id=userid))
    # add user activitiy
    action.send(request.user, verb="added user", action_object=models.User.objects.get(id=userid),
                target=taskgroup)
    return redirect('projectMgr:chooseTaskGroupMates',projectid=projectid,taskGroupId=taskGroupId)


def chooseTaskGroupMates2(request: HttpRequest, projectid, taskGroupId):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    thisTaskGroup = models.TaskGroup.objects.get(id=taskGroupId)
    thisTaskProject = thisTaskGroup.project
    result = thisTaskProject.people.all().exclude(
        username__in=[person.username for person in thisTaskGroup.people.all()])[:20]



    if request.method == 'POST':
        form = forms.chooseMates2(request.POST)
        if form.is_valid():

            search = form.cleaned_data['search']
            searchType = form.cleaned_data['searchType']
            if searchType == 'email':
                result = thisTaskProject.people.filter(email__contains=search).exclude(
                    username__in=[person.username for person in thisTaskGroup.people.all()])[:20]
            elif searchType == 'username':
                result = thisTaskProject.people.filter(username__contains=search).exclude(
                    username__in=[person.username for person in thisTaskGroup.people.all()])[:20]

    else:
        form = forms.chooseMates2()
    return render(request, 'projectMgr/selectTaskGroupMates.html',
                  {'form':form,'results':result, 'project': models.Project.objects.get(id=projectid), 'task': thisTaskGroup, "thisUser": request.user})


def chooseTaskMates(request: HttpRequest, projectid, taskGroupId, taskid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    thisTask = models.Task.objects.get(id=taskid)
    thisTaskGroup = models.TaskGroup.objects.get(id=taskGroupId)
    thisTaskProject = thisTaskGroup.project

    result = thisTaskGroup.people.all().exclude(username__in=[person.username for person in thisTask.people.all()])[:20]

    peopleChoice = [
        [user.username, (user.username + '\t' + user.email)] if user.email else [user.username, (user.username)] for
        user in result]

    if request.method == 'POST':
        form = forms.chooseMates(request.POST, peopleChoice=peopleChoice)
        if form.is_valid():
            selectedPeople = form.cleaned_data.get('people')
            if len(selectedPeople) > 0:
                for personName in selectedPeople:
                    person = models.User.objects.get(username=personName)
                    thisTask.people.add(person)
                thisTask.save()

            if "Done" in request.POST:
                return redirect('projectMgr:taskDetail', projectid=thisTaskProject.id,
                                taskGroupId=thisTaskGroup.id, taskid=taskid)

            search = form.cleaned_data['search']
            searchType = form.cleaned_data['searchType']
            if searchType == 'email':
                result = thisTaskGroup.people.filter(email__contains=search)
            elif searchType == 'username':
                result = thisTaskGroup.people.filter(username__contains=search)

            result = result.exclude(username__in=[person.username for person in thisTask.people.all()])[:20]

            peopleChoice = [
                [user.username, (user.username + '\t' + user.email)] if user.email else [user.username, (user.username)]
                for user in result]

            form = forms.chooseMates(request.POST, peopleChoice=peopleChoice)

    else:
        form = forms.chooseMates(peopleChoice=peopleChoice)
    return render(request, 'projectMgr/selectTaskMates.html',
                  {'form': form, 'project': thisTaskProject, 'taskGroup': thisTaskGroup, 'task': thisTask, "thisUser": request.user})


def addToTask(request:HttpRequest,projectid,taskGroupId,taskid,userid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')
    task = models.Task.objects.get(id=taskid)
    task.people.add(models.User.objects.get(id=userid))
    # added taskmate activitiy
    action.send(request.user, verb="added user", action_object=models.User.objects.get(id=userid),
                target=task)
    return redirect('projectMgr:chooseTaskMates',taskid=taskid,projectid=projectid,taskGroupId=taskGroupId)


def chooseTaskMates2(request: HttpRequest, projectid, taskGroupId, taskid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    thisTask = models.Task.objects.get(id=taskid)
    thisTaskGroup = models.TaskGroup.objects.get(id=taskGroupId)
    thisTaskProject = thisTaskGroup.project

    result = thisTaskGroup.people.all().exclude(username__in=[person.username for person in thisTask.people.all()])[:20]

    if request.method == 'POST':
        form = forms.chooseMates2(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            searchType = form.cleaned_data['searchType']
            if searchType == 'email':
                result = thisTaskGroup.people.filter(email__contains=search)
            elif searchType == 'username':
                result = thisTaskGroup.people.filter(username__contains=search)

            result = result.exclude(username__in=[person.username for person in thisTask.people.all()])[:20]

    else:
        form = forms.chooseMates()
    return render(request, 'projectMgr/selectTaskMates.html',
                  {'results':result,'form': form, 'project': thisTaskProject, 'taskGroup': thisTaskGroup, 'task': thisTask, "thisUser": request.user})


def taskCreate(request: HttpRequest, projectid, taskGroupId):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    '''
    the tasks needs to have a group of people working on it.
    :param request:
    :param projectId:
    :param taskGroupId:
    :return:
    '''
    print('came into task create')
    thisProject = models.Project.objects.get(id=projectid)
    thisTaskGroup = models.TaskGroup.objects.get(id=taskGroupId)


    if request.method == 'POST':
        form = forms.createTask(request.POST)
        if form.is_valid():
            taskName = form.cleaned_data['name']
            description = form.cleaned_data['description']
            stage = form.cleaned_data['stage']
            priority = form.cleaned_data['priority']
            newTask = models.Task.objects.create(name=taskName, description=description, taskGroup=thisTaskGroup,
                                                 reporter=request.user, stage=stage,priority=priority)
            newTask.people.add(request.user)
            newTask.save()
            thisTaskGroup.task_set.add(newTask)
            thisTaskGroup.save()

            # create task activitiy
            action.send(request.user, verb="added task", action_object=newTask,target=thisTaskGroup)
            if "Choose team" in request.POST:
                return redirect("projectMgr:chooseTaskMates", projectid=projectid, taskGroupId=taskGroupId,
                                taskid=newTask.id)
            else:
                return redirect("projectMgr:taskDetail", projectid=projectid, taskGroupId=taskGroupId,
                                taskid=newTask.id)

    else:
        form = forms.createTask()

    return render(request, 'projectMgr/createTask.html',
                  {'project': thisProject, 'taskGroup': thisTaskGroup, 'form': form, "thisUser": request.user})


def taskDelete(request: HttpRequest, projectid, taskGroupId):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    # delete task activitiy
    action.send(request.user, verb="deleted taskgroup", action_object=models.TaskGroup.objects.get(id=taskGroupId), target=models.Project.objects.get(id=projectid))
    taskGroup = models.TaskGroup.objects.get(id=taskGroupId)
    taskGroup.project = None
    taskGroup.save()

    return redirect('projectMgr:projectDetail', projectid=projectid)
    pass


def taskMateRemove(request: HttpRequest, projectid, taskGroupId, taskid, userid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')
    # delete user activitiy
    action.send(request.user, verb="removed user", action_object=models.User.objects.get(id=userid),
                target=models.Task.objects.get(id=taskid))
    models.Task.objects.get(id=taskid).people.remove(models.User.objects.get(id=userid))
    return redirect('projectMgr:taskDetailEdit', projectid, taskGroupId, taskid)


def projectMateRemove(request: HttpRequest, projectid, userid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')
    # delete user activitiy
    action.send(request.user, verb="removed user", action_object=models.User.objects.get(id=userid),
                target=models.Project.objects.get(id=projectid))
    '''
    need to remove user from the project, taskgroups and tasks.
    '''
    project = models.Project.objects.get(id=projectid)
    user = models.User.objects.get(id=userid)
    for taskgroup in project.taskgroup_set:
        if user in taskgroup.people:
            for task in taskgroup.task_set:
                if user in task.people:
                    task.people.remove(user)
                taskgroup.people.remove(user)
    project.people.remove(user)

    return redirect("projectMgr:projectDetailEdit", projectid)


def taskGroupMateRemove(request: HttpRequest, projectid, taskGroupId, userid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    # delete user activitiy
    action.send(request.user, verb="removed user", action_object=models.User.objects.get(id=userid),
                target=models.TaskGroup.objects.get(id=taskGroupId))
    models.TaskGroup.objects.get(id=taskGroupId).people.remove(models.User.objects.get(id=userid))
    return redirect("projectMgr:taskGroupDetailEdit", projectid, taskGroupId)


def taskRemove(request:HttpRequest,projectid,taskGroupId,taskid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    thisTask = models.Task.objects.get(id=taskid)
    thisTask.taskGroup = None
    thisTask.save()


    # delete task activitiy
    action.send(request.user, verb="deleted task", action_object=thisTask,
                target=models.TaskGroup.objects.get(id=taskGroupId))

    # models.Task.objects.get(id=taskid).delete()
    return redirect("projectMgr:taskGroupDetailEdit", projectid, taskGroupId)


def taskGroupRemove(request:HttpRequest,projectid,taskGroupId):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    thistaskGroup = models.TaskGroup.objects.get(id=taskGroupId)
    # delete taskGroup activitiy
    action.send(request.user, verb="deleted taskgroup", action_object=thistaskGroup,
                    target=models.Project.objects.get(id=projectid))
    thistaskGroup.project = None
    thistaskGroup.save()
    return redirect("projectMgr:projectDetailEdit", projectid)


def taskDetailEdit(request: HttpRequest, projectid, taskGroupId, taskid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    '''

    :param request:
    :return:
    '''
    thisProject = models.Project.objects.get(id=projectid)
    thisTaskGroup = models.TaskGroup.objects.get(id=taskGroupId)
    thisTask = models.Task.objects.get(id=taskid)

    if request.method == "POST":
        form = forms.editTask(request.POST, nameVal=thisTask.name, descriptionVal=thisTask.description,
                              stageVal=thisTask.stage, priority=thisTask.priority)

        print('form start', form, 'form end')
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            stage = form.cleaned_data['stage']
            priority = form.cleaned_data['priority']
            thisTask.name = name
            thisTask.description = description
            thisTask.stage = stage
            thisTask.priority = priority
            thisTask.save()
            # edit task activitiy
            action.send(request.user, verb="edited task", action_object= thisTask,
                        target=models.TaskGroup.objects.get(id=taskGroupId))
            return redirect('projectMgr:taskDetail', projectid, taskGroupId, taskid)
    else:
        form = forms.editTask(nameVal=thisTask.name, descriptionVal=thisTask.description, stageVal=thisTask.stage,
                              priority=thisTask.priority)

    return render(request, 'projectMgr/taskDetailEdit.html',
                  {"form": form, "project": thisProject, "taskGroup": thisTaskGroup, "task": thisTask,
                   "thisUser": request.user})


def taskGroupDetail(request: HttpRequest, projectid, taskGroupId):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    '''
    :param request:
    :return:
    '''
    print('received', projectid, taskGroupId)
    thisTaskGroup = models.TaskGroup.objects.get(id=taskGroupId)
    project = models.Project.objects.get(id=projectid)
    commentForm = forms.createComment()
    commentSet = thisTaskGroup.comment.all()
    openTaskSet = thisTaskGroup.task_set.filter(stage='OpenedIssue')
    InProgressTaskSet = thisTaskGroup.task_set.filter(stage='InProgress')
    InReviewTaskSet = thisTaskGroup.task_set.filter(stage='InReview')
    ClosedTaskSet = thisTaskGroup.task_set.filter(stage='ClosedIssue')
    stream = target_stream(thisTaskGroup)
    return render(request, 'projectMgr/taskGroupDetail.html',
                  {'project': project, 'taskGroup': thisTaskGroup, 'commentForm': commentForm, 'commentSet': commentSet,
                   'thisUser': request.user, 'OpenIssue': openTaskSet, 'InProgress': InProgressTaskSet,
                   'InReview': InReviewTaskSet, "ClosedIssue": ClosedTaskSet,'stream':stream})


def taskGroupCreate(request: HttpRequest, projectid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    '''

    :param request:
    :return:
    '''
    print(request.method)
    print(request.POST)
    thisProject = models.Project.objects.get(id=projectid)

    if request.method == "POST":
        form = forms.createTaskgroup(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            newTaskGroup = models.TaskGroup.objects.create(name=name, description=description, creator=request.user,created=datetime.now)
            newTaskGroup.people.add(request.user)
            newTaskGroup.save()
            thisProject = models.Project.objects.get(id=projectid)
            thisProject.taskgroup_set.add(newTaskGroup)
            thisProject.save()
            # create taskgroup activitiy
            action.send(request.user, verb="added taskgroup", action_object=newTaskGroup,
                        target=thisProject)
            # print('projectid',projectid,'taskgroupid',newTask.id)
            if "Choose team" in request.POST:
                return redirect('projectMgr:chooseTaskGroupMates', projectid=projectid, taskGroupId=newTaskGroup.id)
            else:
                return redirect('projectMgr:taskGroupDetail', projectid=projectid, taskGroupId=newTaskGroup.id)

    else:
        form = forms.createTaskgroup()

    return render(request, "projectMgr/createTaskGroup.html", {'form': form, 'project': thisProject, "thisUser": request.user})


def deleteComment(commentid):

    thisComment = models.Comment.objects.get(id=commentid)
    thisComment.deleted = True
    thisComment.save()


def taskDeleteComment(request: HttpRequest, projectid, taskGroupId, taskid, commentid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    deleteComment(commentid)
    return redirect('projectMgr:taskDetail', projectid, taskGroupId, taskid)


def taskGroupDeleteComment(request: HttpRequest, projectid, taskGroupId, commentid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    deleteComment(commentid)
    return redirect('projectMgr:taskGroupDetail', projectid, taskGroupId)


def projectDeleteComment(request: HttpRequest, projectid, commentid):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    deleteComment(commentid)
    return redirect('projectMgr:projectDetail', projectid)


def userinfo(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    return render(request,'projectMgr/userinfo.html',{'thisUser':request.user})

def fileHandler(file, destination):

    with open(destination,'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

def deleteFile(path):

    import os
    if (path and os.path.exists(path)):
        os.remove(path)

def uploadProfilePic(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('projectMgr:homepage')

    form = forms.uploadProfilePic(request.POST, request.FILES)


    if form.is_valid():

        from django.conf import settings

        # print(settings.MEDIA_ROOT, 'media root')
        # path = settings.MEDIA_URL
        #delete previous image
        # print('media root',settings.MEDIA_ROOT)
        path = settings.MEDIA_ROOT+'/projectMgr/'+request.FILES['image']._get_name()
        thisUserObject = models.User.objects.get(id=request.user.id)
        currentPath = thisUserObject.profilePicture
        deleteFile(currentPath)
        thisUserObject.profilePicture = '/media/projectMgr/'+request.FILES['image']._get_name()
        print(thisUserObject.profilePicture)
        thisUserObject.save()
        print(request.FILES['image']._get_name())
        fileHandler(request.FILES['image'], path)

        return redirect('projectMgr:userinfo')

    return render(request, 'projectMgr/uploadImage.html',{'thisUser':request.user, 'form':form})

#rest framework viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskGroupViewSet(viewsets.ModelViewSet):
    queryset = models.TaskGroup.objects.all()
    serializer_class = TaskGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
