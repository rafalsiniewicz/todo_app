from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app.forms import TODOForm, TeamForm, CommentForm, CustomizedUserCreationForm
from app.models import TODO, Team, User, UserInfo, PrivateConversation
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


# Create your views here.

@login_required(login_url='login')
def home(request, team_id = 0):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        teams = Team.objects.filter(users=user)
        team = None
        todos = []
        messages = []
        if team_id == 0:
            if len(teams) > 0:
                team = teams.first()
                messages = team.messages.all()
                team_id = team.id
        if team_id != 0:
            try:
                team = teams.get(id=team_id)
                messages = team.messages.all()
            except Team.DoesNotExist:
                team = None
        if team != None:
            todos = team.todos.order_by('-priority')
        stats = {st: 0 for st in ['Done', 'In_progress', 'To_do', 'Expired']}
        for status in list(map(lambda t: t.status, todos)):
            stats[status.replace(' ', '_')] += 1
        return render(request, 'index.html', context={'form': form, 'todos': todos, 'stats': stats, 'teams': teams, 'team': team, 'team_id': team_id, 'messages': messages, 'user': user})


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm
        context = {
            "form": form
        }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                ui = UserInfo.objects.get(user=user)
                ui.status = "AVAILABLE",
                ui.save(),
                return redirect('home')
        else:
            context = {
                "form": form
            }
            return render(request, 'login.html', context=context)


def signup(request):
    if request.method == 'GET':
        form = CustomizedUserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)
    else:
        form = CustomizedUserCreationForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                ui = UserInfo()
                ui.user = user
                ui.status = 'OFFLINE'
                ui.save()
                return redirect('login')
        else:
            return render(request, 'signup.html', context=context)


@login_required(login_url='login')
def add_todo(request, team_id):
    if request.user.is_authenticated:
        form = TODOForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            todo = form.save(commit=False)
            todo.save()
            team = Team.objects.get(pk=team_id)
            team.todos.add(todo)
            team.save()
            user.email_user(subject='You have new task',
                            message='Hello from todo_app. You have new task assigned. This message is automated, please don\'t reply.',
                            )
            return redirect("home")
        else:
            context = {
                'form': form
            }
            return render(request, 'index.html', context=context)


def add_comment(request, id):
    if request.user.is_authenticated:
        todo = TODO.objects.get(pk=id)
        user = request.user
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.author = user
        comment.save()
        todo.comments.add(comment)
        todo.save()
        return redirect('/todo/' + str(id) + '/comments')

def add_message(request, team_id):
     if request.user.is_authenticated:
        team = Team.objects.get(pk=team_id)
        user = request.user
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.author = user
        comment.save()
        team.messages.add(comment)
        team.save()
        return redirect('/home/' + str(team_id))

def add_private_message(request, user_id, second_user_id, conversation_id):
     if request.user.is_authenticated:
        conversation = PrivateConversation.objects.get(pk=conversation_id)
        user = request.user
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.author = user
        comment.save()
        conversation.messages.add(comment)
        conversation.save()
        return redirect('/private_conversation/' + str(user_id) + '/' + str(second_user_id))

def delete_todo(request, id):
    TODO.objects.get(pk=id).delete()
    return redirect('home')


def change_todo(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect('home')


def todo_comments(request, id):
    if request.user.is_authenticated:
        todo = TODO.objects.get(pk=id)
        form = CommentForm()
        comments = todo.comments.all()
        context = {'form': form, 'comments': comments, 'todo': todo}
        return render(request, 'todo_comments.html', context=context)


def signout(request):
    user = request.user
    ui = UserInfo.objects.get(user=user)
    ui.status = "OFFLINE",
    ui.save(),
    logout(request)
    return redirect('login')


def teams(request):
    if request.user.is_authenticated:
        user = request.user
        form = TeamForm()
        teams = Team.objects.filter(owner=user).order_by('-title')
        context = {'form': form, 'teams': teams}
        return render(request, 'teams.html', context=context)


def team_users(request, id):
    if request.user.is_authenticated:
        user = request.user
        team = Team.objects.get(pk=id)
        users = team.users.all()
        context = {'team': team, 'users': users, 'user': user}
        return render(request, 'team_users.html', context=context)

def private_conversation(request, user_id, second_user_id):
    if request.user.is_authenticated:
        user = request.user
        second_user = User.objects.get(pk=second_user_id)
        conversations = PrivateConversation.objects.filter(users=user)
        conversations = conversations.filter(users=second_user)
        conversation = None
        messages = []
        if len(conversations) == 0:
            conversation = PrivateConversation()
            conversation.save()
            conversation.users.add(user)
            conversation.users.add(second_user)
            conversation.save()
        else:
            conversation = conversations.first()
            messages = conversation.messages.all()
        context = {'user_id' : user_id, 'second_user_id': second_user_id, 'conversation_id': conversation.id, 'messages': messages}
        return render(request, 'private_conversation.html', context=context)


def team_members_add_view(request, id):
    if request.user.is_authenticated:
        user = request.user
        team = Team.objects.get(pk=id)
        users = User.objects.all()
        team_users_list = list(team.users.all())
        users_list = list(filter(lambda x: x not in team_users_list, list(users)))
        context = {'users': users, 'team': team, 'users_list': users_list}
        return render(request, 'team_members_add.html', context=context)


def add_member_to_team(request, id, user_id):
    if request.user.is_authenticated:
        team = Team.objects.get(pk=id)
        user = User.objects.get(pk=user_id)
        team.users.add(user)
        team.save()
        return redirect('/teams/team_users/' + str(id))


def remove_member_from_team(request, id, user_id):
    if request.user.is_authenticated:
        team = Team.objects.get(pk=id)
        user = User.objects.get(pk=user_id)
        team.users.remove(user)
        team.save()
        return redirect('/teams/team_users/' + str(id))

def leave_team(request, team_id):
    if request.user.is_authenticated:
        team = Team.objects.get(pk=team_id)
        user = request.user
        team.users.remove(user)
        team.save()
        return redirect('/home/0')


def add_team(request):
    if request.user.is_authenticated:
        user = request.user
        form = TeamForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.owner = user
            todo.save()
            todo.users.add(user)
            todo.save()
            return redirect("teams")