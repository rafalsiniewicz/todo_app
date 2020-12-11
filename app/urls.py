"""todo_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from app.views import home, login, signup, add_todo, signout, delete_todo, change_todo, teams, add_team, team_users, \
    team_members_add_view, add_member_to_team, remove_member_from_team, todo_comments, add_comment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('signup/', signup),
    path('add-todo/', add_todo),
    path('add-comment/<int:id>', add_comment),
    path('todo/<int:id>/comments', todo_comments),
    path('delete-todo/<int:id>', delete_todo),
    path('change-status/<int:id>/<str:status>', change_todo),
    path('logout/', signout),
    path('teams/', teams, name="teams"),
    path('add-team/', add_team),
    path('teams/team_users/<int:id>', team_users),
    path('teams/team_users/<int:id>/add', team_members_add_view),
    path('teams/team_users/<int:id>/add/<int:user_id>', add_member_to_team),
    path('teams/team_users/<int:id>/remove/<int:user_id>', remove_member_from_team)
]
