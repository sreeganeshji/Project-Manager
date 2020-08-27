"""ProjectManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


app_name = 'projectMgr'

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signUp,name='signup'),
    path('userhome/',views.userHome,name='userhome'),
    path('logout/',views.logoutReq,name='logout'),
    path('<int:projectid>/<int:taskGroupId>/createTask/', views.taskCreate, name='createTask'),
    path('<int:projectid>/chooseProjectMates/',views.chooseProjectMates2,name='chooseProjectMates'),
    path('<int:projectid>/<int:taskGroupId>/<int:taskid>/task/',views.taskDetail,name='taskDetail'),
    path('<int:projectid>/<int:taskGroupId>/<int:taskid>/<int:userid>/addToTask/', views.addToTask,name='addToTask'),
    path('<int:projectid>/<int:taskGroupId>/<int:taskid>/chooseTaskMates/',views.chooseTaskMates2,name='chooseTaskMates'),
    path('createProject/',views.projectCreate,name='projectCreate'),
    path('<int:projectid>/project/',views.projectDetail,name='projectDetail'),
    path('<int:projectid>/<int:userid>/addToProject',views.addToProject,name='addToProject'),
    path('<int:projectid>/projectDetailComment',views.projectDetailComment,name="projectDetailComment"),
    path('<int:projectid>/projectEdit/',views.projectDetailEdit,name='projectDetailEdit'),
    path('<int:projectid>/<int:taskGroupId>/<int:taskid>/taskEdit/',views.taskDetailEdit,name='taskDetailEdit'),
    path('<int:projectid>/<int:taskGroupId>/<int:taskid>/<int:userid>/taskMateRemove',views.taskMateRemove,name='taskMateRemove'),
    path('<int:projectid>/<int:userid>/removeProjectMates',views.projectMateRemove,name="projectMateRemove"),
    path('<int:projectid>/<int:taskGroupId>/removeTaskGroup', views.taskGroupRemove, name="taskGroupRemove"),
    path('<int:projectid>/<int:taskGroupId>/<int:userid>/taskGroupMateRemove',views.taskGroupMateRemove,name="taskGroupMateRemove"),
    path('<int:projectid>/<int:taskGroupId>/<int:taskid>/taskRemove',views.taskRemove,name="taskRemove"),
    path('<int:projectid>/createTaskGroup/',views.taskGroupCreate,name='createTaskGroup'),
    path('<int:projectid>/<int:taskGroupId>/deleteTaskGroup/',views.taskDelete,name='taskDelete'),
    path('<int:projectid>/<int:taskGroupId>/chooseTaskGroupMates/',views.chooseTaskGroupMates2,name='chooseTaskGroupMates'),
    path('<int:projectid>/<int:taskGroupId>/<int:userid>/addToTaskGroup/', views.addToTaskGroup, name='addToTaskGroup'),
    path('<int:projectid>/<int:taskGroupId>/taskGroup/',views.taskGroupDetail,name='taskGroupDetail'),
    path('<int:projectid>/<int:taskGroupId>/taskGroupEdit/',views.taskGroupDetailEdit,name='taskGroupDetailEdit'),
    path('<int:projectid>/<int:taskGroupId>/taskGroupDetailComment',views.taskGroupDetailComment,name='taskGroupDetailComment'),
    path('<int:projectid>/<int:taskGroupId>/<int:taskid>/addComment',views.taskDetailComment,name='taskDetailComment'),
    path('<int:projectid>/<int:taskGroupId>/<int:taskid>/<int:commentid>/deleteComment',views.taskDeleteComment,name='taskDeleteComment'),
    path('<int:projectid>/<int:taskGroupId>/<int:commentid>/deleteComment',views.taskGroupDeleteComment,name="taskGroupDeleteComment"),
    path('<int:projectid>/<int:commentid>/deleteComment',views.projectDeleteComment,name='projectDeleteComment'),
    path('about/',views.about,name='about'),
    path('userinfo/',views.userinfo,name='userinfo'),
    path('upload_profile_pic/',views.uploadProfilePic,name='upload_profile_pic'),
    path('<int:projectid>/followProject',views.followProject, name='followProject'),
    path('<int:projectid>/<int:taskGroupId>/followTaskGroup', views.followTaskGroup, name='followTaskGroup'),
    path('<int:projectid>/<int:taskGroupId>/<int:taskid>/followTask', views.followTask, name='followTask'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
