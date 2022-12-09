from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Permission


class MyUsersInline(admin.StackedInline):
    model = MyUsers
    can_delete = False
    verbose_name_plural = 'myusers'


class UserAdmin(BaseUserAdmin):
    inlines = (MyUsersInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(MyUsers)
admin.site.register(BorrowedBooks)
admin.site.register(Librarian)
admin.site.register(Student)


# admin.site.register(MyUsers)
