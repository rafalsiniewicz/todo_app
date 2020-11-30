from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app.forms import TODOForm, TeamForm, CommentForm
from app.models import TODO, Team, User
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user).order_by('-priority')
        stats = {st: 0 for st in ['Done', 'In_progress', 'To_do', 'Expired']}
        for status in list(map(lambda t: t.status, todos)):
            stats[status.replace(' ', '_')] += 1
        return render(request, 'index.html', context={'form': form, 'todos': todos, 'stats': stats})

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
                return redirect('home')
        else:
            context = {
                "form": form
            }
            return render(request, 'login.html', context=context)


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)
    else:
        form = UserCreationForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'signup.html', context=context)

@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return redirect("home")
        else:
            context = {
                'form': form
            }
            return render(request, 'index.html', context=context)

def add_comment(request, id):
    if request.user.is_authenticated:
        todo = TODO.objects.get(pk = id)
        user = request.user
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.author = user
        comment.save()
        todo.comments.add(comment)
        todo.save()
        print(comment.content)
        return redirect('/todo/' + str(id) + '/comments')

def delete_todo(request, id):
    TODO.objects.get(pk = id).delete()
    return redirect('home')

def change_todo(request, id, status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')

def todo_comments(request, id):
    if request.user.is_authenticated:
        todo = TODO.objects.get(pk = id)
        form = CommentForm()
        comments = todo.comments.all()
        context = {'form': form, 'comments': comments, 'todo': todo}
        return render(request, 'todo_comments.html', context=context)

def signout(request):
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
        context = {'team': team, 'users': users}
        return render(request, 'team_users.html', context=context)

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
        team = Team.objects.get(pk = id)
        user = User.objects.get(pk = user_id)
        team.users.add(user)
        team.save()
        return redirect('/teams/team_users/' + str(id))

def remove_member_from_team(request, id, user_id):
    if request.user.is_authenticated:
        team = Team.objects.get(pk = id)
        user = User.objects.get(pk = user_id)
        team.users.remove(user)
        team.save()
        return redirect('/teams/team_users/' + str(id))

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


