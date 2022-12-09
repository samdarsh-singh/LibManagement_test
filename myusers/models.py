from django.db import models
from django.contrib.auth.models import User, Permission
# Create your models here.


class MyUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_librarian = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    copies = models.IntegerField(default=1)
    available = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class BorrowedBooks(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    date_borrowed = models.DateField(auto_now_add=True)
    date_returned = models.DateField(null=True, blank=True)
    renewed = models.BooleanField(default=False)

    def __str__(self):
        return self.book.title


class Librarian(models.Model):
    user = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username

class Student(models.Model):
    user = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    borrow = models.IntegerField(default=0)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username