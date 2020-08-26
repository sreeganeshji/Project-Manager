from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class signUp(UserCreationForm):
    email = forms.EmailField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email','password1','password2']
    pass


class signIn(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)


class createProject(forms.Form):
    '''
    create Project
    name
    description
    people
    '''
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, required=False)


    pass


class chooseMates2(forms.Form):
    search = forms.CharField(max_length=200, required=False)
    searchType = forms.ChoiceField(choices=[['username', 'username'], ['email', 'email']], required=False,
                                   widget=forms.RadioSelect, initial='email')



#depreciated
class chooseMates(forms.Form):
    '''
    have the user enter the emailid of the other users and press the search key.
    the search results should include the email id and the username. or we can have a selector whcih chooses
    between the two.
    '''

    search = forms.CharField(max_length=200,required=False)
    searchType = forms.ChoiceField(choices=[['username','username'],['email','email']],required=False,widget=forms.RadioSelect,initial='email')
    people = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,required=False)

    def __init__(self,  *args, peopleChoice=None, **kwargs):
        print("peopleChoice",peopleChoice)
        super().__init__(*args,**kwargs)
        if peopleChoice:
            # self.people.choices = peopleChoice
            self.fields['people'].choices = peopleChoice


class editTask(forms.Form):
    name = forms.CharField(max_length=100,required=False)
    description = forms.CharField(widget=forms.Textarea,empty_value="description default")
    stage = forms.ChoiceField(choices=[['OpenedIssue','OpenedIssue'],['InProgress','InProgress'],['InReview','InReview'],['ClosedIssue','ClosedIssue']])
    priority = forms.ChoiceField(choices=[["Urgent", "Urgent"], ['High', 'High'], ['Normal', 'Normal'], ['low', 'low']])
    def __init__(self,*args,nameVal=None,descriptionVal=None,stageVal=None,priority=None,**kwargs):
        super().__init__(*args,**kwargs)
        print("name is ",nameVal)
        if nameVal:
            self.fields['name'].initial = nameVal
        if descriptionVal:
            self.fields['description'].initial = descriptionVal
        if stageVal:
            self.fields['stage'].initial = stageVal
        if priority:
            self.fields['priority'].initial = priority


class editTaskGroup(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    description = forms.CharField(widget=forms.Textarea, empty_value="description default")

    def __init__(self, *args, nameVal=None, descriptionVal=None, **kwargs):
        super().__init__(*args, **kwargs)
        print("name is ", nameVal)
        if nameVal:
            self.fields['name'].initial = nameVal
        if descriptionVal:
            self.fields['description'].initial = descriptionVal


class editProject(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    description = forms.CharField(widget=forms.Textarea, empty_value="description default")

    def __init__(self, *args, nameVal=None, descriptionVal=None, **kwargs):
        super().__init__(*args, **kwargs)
        print("name is ", nameVal)
        if nameVal:
            self.fields['name'].initial = nameVal
        if descriptionVal:
            self.fields['description'].initial = descriptionVal


class createTaskgroup(forms.Form):
    '''
    name
    description
    tasks:
    '''
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea,required=False)

    pass


class createTask(forms.Form):
    '''
    name
    description
    created
    modified
    deadline(optional)
    comments

    '''
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, required=False)
    stage = forms.ChoiceField(choices=[['OpenedIssue', 'OpenedIssue'], ['InProgress', 'InProgress'], ['InReview', 'InReview'],
                 ['ClosedIssue', 'ClosedIssue']])
    priority = forms.ChoiceField(choices=[['Normal', 'Normal'], ["Urgent", "Urgent"], ['High', 'High'], ['low', 'low']])


class createComment(forms.Form):
    '''
    textField
    to handle whether a first comment or a reply in the models.
    '''
    Comment = forms.CharField(widget=forms.TextInput,max_length=500)
    pass


class uploadImage(forms.Form):
    '''
    title
    file
    '''
    title = forms.CharField(max_length=100)
    file = forms.FileField()

class uploadProfilePic(forms.Form):
    image = forms.FileField()