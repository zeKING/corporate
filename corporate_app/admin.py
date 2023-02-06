from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
class CustomUserAdmin(UserAdmin):
    ordering = ('email', )
    list_display = ('fio', 'email', 'avatar', 'role')
    search_fields = ("fio", "email", "role")
    fieldsets = (
        (None, {"fields": ("fio", "password", "role", "avatar")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("fio", "email", "password1", "password2", "avatar"),
            },
        ),
    )

class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'file', 'created', 'from_user', 'to_user')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Tasks)
admin.site.register(RolePermission)
admin.site.register(Folders)
admin.site.register(Files)
admin.site.register(Message, MessageAdmin)
admin.site.register(Dialog)
