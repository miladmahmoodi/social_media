from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as UserModel

from .models import(
    Relation as RelationModel,
    Profile as ProfileModel,
)


class ProfileInline(admin.StackedInline):
    model = ProfileModel
    can_delete = False


class NewUserAdmin(UserAdmin):
    inlines = (
        ProfileInline,
    )


admin.site.unregister(
    UserModel,
)
admin.site.register(
    UserModel,
    NewUserAdmin,
)
admin.site.register(
    RelationModel,
)
