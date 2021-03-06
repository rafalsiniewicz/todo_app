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
    team_members_add_view, add_member_to_team, remove_member_from_team, todo_comments, add_comment, add_message, \
    leave_team, private_conversation, add_private_message, stats, settings, change_password, change_github, change_style

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/<int:team_id>', home),
    path('leave_team/<int:team_id>', leave_team),
    path('login/', login, name='login'),
    path('signup/', signup),
    path('add-todo/<int:team_id>', add_todo),
    path('add-comment/<int:id>', add_comment),
    path('todo/<int:id>/comments', todo_comments),
    path('add-message/<int:team_id>', add_message),
    path('add_private_message/<int:user_id>/<int:second_user_id>/<int:conversation_id>', add_private_message),
    path('delete-todo/<int:id>', delete_todo),
    path('change-status/<int:id>/<str:status>', change_todo),
    path('logout/', signout),
    path('teams/', teams),
    path('settings/', settings),
    path('settings/change-password', change_password),
    path('settings/change-github', change_github),
    path('settings/change-style/<str:style>', change_style),
    path('add-team/', add_team),
    path('private_conversation/<int:user_id>/<int:second_user_id>', private_conversation),
    path('teams/team_users/<int:id>', team_users),
    path('teams/team_users/<int:id>/add', team_members_add_view),
    path('teams/team_users/<int:id>/add/<int:user_id>', add_member_to_team),
    path('teams/team_users/<int:id>/remove/<int:user_id>', remove_member_from_team),
    path('statistics/', stats),
]
