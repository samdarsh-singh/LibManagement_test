"""libsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from myusers.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path("student/register/", StudentRegister.as_view()  , name="student_register"),
    path("lib/register/", LibrarianRegister.as_view()  , name="student_register"),
    path("login/", LoginView.as_view()  , name="student_login"),
    path("book/post", BookPostView.as_view()  , name="book_post"),
    path("book/borrow", BorrowbookView.as_view()  , name="book_borrow"),
    path("book/return", ReturnBookView.as_view()  , name="book_return"),
]
