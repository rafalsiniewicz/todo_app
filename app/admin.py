from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from app.models import TODO, Team, UserInfo, PrivateConversation, Comment

# Register your models here.
admin.site.register(TODO)
admin.site.register(Team)
admin.site.register(UserInfo)
admin.site.register(Comment)
admin.site.register(PrivateConversation)

class UserInfoInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name_plural = 'userInfo'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserInfoInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
