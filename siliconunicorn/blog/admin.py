from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UnicornUserCreationForm, UnicornUserChangeForm
from .models import UnicornUser, Post, Comment, Tag

###
#Admin actions
###
def activate(modeladmin, request, queryset):
    queryset.update(active=True)
    activate.short_description = "Activate selected entries"

def deactivate(modeladmin, request, queryset):
    queryset.update(active=False)
    deactivate.short_description = "Deactivate selected entries"

###
#Admin classes
###

class UnicornUserAdmin(UserAdmin):
    add_form = UnicornUserCreationForm
    form = UnicornUserChangeForm
    model = UnicornUser
    list_display = ['username','email', 'is_staff', 'is_superuser', 'last_login']


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'slug', 'date_published',  'like_count', 'comment_count', 'active' ]
    prepopulated_fields = {'slug': ('title',)}
    actions = [activate, deactivate]

class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'display_author', 'content', 'timestamp', 'parent_post', 'active']
    actions = [activate, deactivate]


admin.site.register(UnicornUser, UnicornUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
