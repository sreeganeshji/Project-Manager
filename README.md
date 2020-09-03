# Project-Manager
Web application for collaborative project management and issue tracking.
# Features
* Create  **Projects**, **Task-Groups** and **Tasks**.
* Assign priorities to the **Tasks** from Low, Normal, High and Urgent.
* Interact with the team using the comments under each **Project**, **Task-Group** and **Task**.
* Follow the events pertaining to each **Project**, **Task-Group** and **Task** which will be published on the homepage. 
* Provides REST API endpoints which allows for third-party integration.
# Preview
**Task-Group:** The **Tasks** are presented on the kanban board based on their stage and colored based on their priority.
<image src="https://raw.githubusercontent.com/sreeganeshji/Project-Manager/master/Illustrations/taskGroup.jpg" width=2200>

**Project:** 
* The project page lists all the teammates on the sidebar.
* You can interact with the team in the comments section.
<image src="https://raw.githubusercontent.com/sreeganeshji/Project-Manager/master/Illustrations/project.jpg" width=2200>

**Homepage:**
* The homepage lists all the tasks that are assigned to you.
* Below, the notification presents all the events that you follow.
<image src="https://raw.githubusercontent.com/sreeganeshji/Project-Manager/master/Illustrations/userhome.jpg" width=2200>

# Frameworks used
* The web framework used is [Django](https://www.djangoproject.com).
* Notification system was implemented using [Django Activity Stream](https://django-activity-stream.readthedocs.io/en/latest/) framework.
* Authentication system was supported by the [Django allauth](https://github.com/pennersr/django-allauth) framework.
* REST framework endpoints were implemented using the [Django-Restframework](https://www.django-rest-framework.org/api-guide/permissions/).
