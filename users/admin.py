
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


class UserModelAdmin(BaseUserAdmin):
    
    list_display = ('username','employee_id', 'is_active', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        ('User Credentials', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ( 'email', 'first_name', 'last_name', 'employee_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    search_fields = ('username', 'email')  
    ordering = ('username',) 
    filter_horizontal = ()

admin.site.register(User, UserModelAdmin)
